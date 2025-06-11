import json
import asyncio
from typing import Dict, List, Optional, AsyncGenerator, Any
from enum import Enum
import httpx
from openai import AsyncOpenAI
import dashscope
from dashscope import Generation
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import settings


class LLMProvider(str, Enum):
    """大模型提供商枚举"""
    TONGYI = "tongyi"  # 通义千问
    DEEPSEEK = "deepseek"  # DeepSeek
    DOUBAO = "doubao"  # 豆包
    GEMINI = "gemini"  # Gemini
    CUSTOM = "custom"  # 自定义


class LLMConfig:
    """大模型配置"""
    def __init__(self, provider: LLMProvider, api_key: str, model: str = None, base_url: str = None):
        self.provider = provider
        self.api_key = api_key
        self.model = model or self._get_default_model(provider)
        self.base_url = base_url or self._get_default_base_url(provider)
    
    def _get_default_model(self, provider: LLMProvider) -> str:
        """获取默认模型"""
        defaults = {
            LLMProvider.TONGYI: "qwen-max",
            LLMProvider.DEEPSEEK: "deepseek-chat",
            LLMProvider.DOUBAO: "doubao-pro-4k",
            LLMProvider.GEMINI: "gemini-pro",
            LLMProvider.CUSTOM: "gpt-3.5-turbo"
        }
        return defaults.get(provider, "gpt-3.5-turbo")
    
    def _get_default_base_url(self, provider: LLMProvider) -> str:
        """获取默认API地址"""
        defaults = {
            LLMProvider.TONGYI: "https://dashscope.aliyuncs.com/api/v1",
            LLMProvider.DEEPSEEK: "https://api.deepseek.com/v1",
            LLMProvider.DOUBAO: "https://ark.cn-beijing.volces.com/api/v3",
            LLMProvider.GEMINI: "https://generativelanguage.googleapis.com/v1beta",
            LLMProvider.CUSTOM: "https://api.openai.com/v1"
        }
        return defaults.get(provider)


class LLMService:
    """大模型服务"""
    
    def __init__(self):
        self.clients: Dict[str, Any] = {}
    
    def configure_llm(self, config: LLMConfig) -> str:
        """配置大模型"""
        config_id = f"{config.provider}_{hash(config.api_key)}"
        
        if config.provider == LLMProvider.TONGYI:
            dashscope.api_key = config.api_key
            self.clients[config_id] = {"type": "tongyi", "config": config}
        
        elif config.provider == LLMProvider.DEEPSEEK:
            client = AsyncOpenAI(api_key=config.api_key, base_url=config.base_url)
            self.clients[config_id] = {"type": "openai_compatible", "client": client, "config": config}
        
        elif config.provider == LLMProvider.DOUBAO:
            client = AsyncOpenAI(api_key=config.api_key, base_url=config.base_url)
            self.clients[config_id] = {"type": "openai_compatible", "client": client, "config": config}
        
        elif config.provider == LLMProvider.GEMINI:
            genai.configure(api_key=config.api_key)
            self.clients[config_id] = {"type": "gemini", "config": config}
        
        elif config.provider == LLMProvider.CUSTOM:
            client = AsyncOpenAI(api_key=config.api_key, base_url=config.base_url)
            self.clients[config_id] = {"type": "openai_compatible", "client": client, "config": config}
        
        return config_id
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def analyze_api_document(
        self, 
        config_id: str, 
        document_content: str, 
        document_type: str = "unknown"
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        分析API文档并流式返回解析结果
        
        Args:
            config_id: 大模型配置ID
            document_content: 文档内容
            document_type: 文档类型
        
        Yields:
            解析出的API接口信息
        """
        if config_id not in self.clients:
            raise ValueError(f"LLM配置不存在: {config_id}")
        
        client_info = self.clients[config_id]
        
        # 构建提示词
        prompt = self._build_analysis_prompt(document_content, document_type)
        
        # 根据不同的模型提供商进行处理
        async for result in self._stream_analyze(client_info, prompt):
            yield result
    
    def _build_analysis_prompt(self, content: str, doc_type: str) -> str:
        """构建分析提示词"""
        return f"""
你是一个专业的API文档分析专家。请分析以下{doc_type}类型的API文档内容，并提取出所有API接口信息。

请按照以下JSON格式返回结果，每个API接口一个JSON对象，每行一个：

{{
  "name": "接口名称",
  "description": "接口描述",
  "method": "HTTP方法(GET/POST/PUT/DELETE等)",
  "path": "接口路径",
  "tags": ["标签1", "标签2"],
  "parameters": [
    {{
      "name": "参数名",
      "in": "参数位置(query/path/header/body)",
      "type": "参数类型",
      "required": true/false,
      "description": "参数描述",
      "example": "示例值"
    }}
  ],
  "responses": [
    {{
      "status_code": 200,
      "description": "响应描述",
      "example": "响应示例"
    }}
  ],
  "security": ["认证方式"],
  "notes": "额外说明"
}}

重要要求：
1. 每个API接口输出一行完整的JSON对象
2. 不要输出其他格式的内容
3. 确保JSON格式正确
4. 如果某些字段信息不明确，可以设置为null或空数组
5. 请仔细分析文档，提取所有可识别的API接口

文档内容：
{content}
"""
    
    async def _stream_analyze(self, client_info: Dict, prompt: str) -> AsyncGenerator[Dict[str, Any], None]:
        """流式分析"""
        client_type = client_info["type"]
        config = client_info["config"]
        
        if client_type == "tongyi":
            async for result in self._stream_tongyi(prompt, config):
                yield result
        
        elif client_type == "openai_compatible":
            async for result in self._stream_openai_compatible(client_info["client"], prompt, config):
                yield result
        
        elif client_type == "gemini":
            async for result in self._stream_gemini(prompt, config):
                yield result
    
    async def _stream_tongyi(self, prompt: str, config: LLMConfig) -> AsyncGenerator[Dict[str, Any], None]:
        """通义千问流式处理"""
        try:
            response = Generation.call(
                model=config.model,
                prompt=prompt,
                stream=True,
                result_format='message'
            )
            
            buffer = ""
            for chunk in response:
                if hasattr(chunk, 'output') and hasattr(chunk.output, 'choices'):
                    content = chunk.output.choices[0]['message']['content']
                    buffer += content
                    
                    # 尝试解析完整的JSON行
                    lines = buffer.split('\n')
                    buffer = lines[-1] if lines[-1].strip() else ""
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        if line:
                            try:
                                api_data = json.loads(line)
                                yield {
                                    "type": "api",
                                    "data": api_data,
                                    "status": "success"
                                }
                            except json.JSONDecodeError:
                                continue
            
            # 处理最后的buffer
            if buffer.strip():
                try:
                    api_data = json.loads(buffer.strip())
                    yield {
                        "type": "api",
                        "data": api_data,
                        "status": "success"
                    }
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            yield {
                "type": "error",
                "message": f"通义千问分析出错: {str(e)}",
                "status": "error"
            }
    
    async def _stream_openai_compatible(self, client: AsyncOpenAI, prompt: str, config: LLMConfig) -> AsyncGenerator[Dict[str, Any], None]:
        """OpenAI兼容接口流式处理"""
        try:
            response = await client.chat.completions.create(
                model=config.model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
                temperature=0.1
            )
            
            buffer = ""
            async for chunk in response:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    buffer += content
                    
                    # 尝试解析完整的JSON行
                    lines = buffer.split('\n')
                    buffer = lines[-1] if lines[-1].strip() else ""
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        if line:
                            try:
                                api_data = json.loads(line)
                                yield {
                                    "type": "api",
                                    "data": api_data,
                                    "status": "success"
                                }
                            except json.JSONDecodeError:
                                continue
            
        except Exception as e:
            yield {
                "type": "error",
                "message": f"模型分析出错: {str(e)}",
                "status": "error"
            }
    
    async def _stream_gemini(self, prompt: str, config: LLMConfig) -> AsyncGenerator[Dict[str, Any], None]:
        """Gemini流式处理"""
        try:
            model = genai.GenerativeModel(config.model)
            response = model.generate_content(
                prompt,
                stream=True,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,
                )
            )
            
            buffer = ""
            for chunk in response:
                if chunk.text:
                    buffer += chunk.text
                    
                    # 尝试解析完整的JSON行
                    lines = buffer.split('\n')
                    buffer = lines[-1] if lines[-1].strip() else ""
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        if line:
                            try:
                                api_data = json.loads(line)
                                yield {
                                    "type": "api",
                                    "data": api_data,
                                    "status": "success"
                                }
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            yield {
                "type": "error",
                "message": f"Gemini分析出错: {str(e)}",
                "status": "error"
            }


# 全局实例
llm_service = LLMService() 