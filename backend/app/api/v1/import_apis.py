from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import json
import os
import uuid
from pathlib import Path
from typing import Optional, List

from app.core.database import get_db
from app.core.llm_service import llm_service, LLMConfig, LLMProvider
from app.core.document_parser import document_parser
from app.models.api import API
from app.models.project import Project
from app.schemas.import_schema import (
    LLMConfigRequest, 
    ImportRequest, 
    ImportResponse,
    LLMProviderInfo
)

router = APIRouter()

# 存储文件的目录
UPLOAD_DIR = Path("uploads/documents")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.get("/providers", response_model=List[LLMProviderInfo])
async def get_llm_providers():
    """获取支持的大模型提供商列表"""
    providers = [
        LLMProviderInfo(
            id="tongyi",
            name="通义千问",
            description="阿里云通义千问大语言模型",
            models=["qwen-max", "qwen-plus", "qwen-turbo"],
            default_model="qwen-max",
            api_key_placeholder="sk-xxx",
            base_url="https://dashscope.aliyuncs.com/api/v1"
        ),
        LLMProviderInfo(
            id="deepseek",
            name="DeepSeek",
            description="DeepSeek 大语言模型",
            models=["deepseek-chat", "deepseek-coder"],
            default_model="deepseek-chat",
            api_key_placeholder="sk-xxx",
            base_url="https://api.deepseek.com/v1"
        ),
        LLMProviderInfo(
            id="doubao",
            name="豆包",
            description="字节跳动豆包大语言模型",
            models=["doubao-pro-4k", "doubao-pro-32k", "doubao-lite-4k"],
            default_model="doubao-pro-4k",
            api_key_placeholder="YOUR_API_KEY",
            base_url="https://ark.cn-beijing.volces.com/api/v3"
        ),
        LLMProviderInfo(
            id="gemini",
            name="Gemini",
            description="Google Gemini 大语言模型",
            models=["gemini-pro", "gemini-pro-vision"],
            default_model="gemini-pro",
            api_key_placeholder="AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            base_url="https://generativelanguage.googleapis.com/v1beta"
        ),
        LLMProviderInfo(
            id="custom",
            name="自定义",
            description="自定义OpenAI兼容接口",
            models=["gpt-3.5-turbo", "gpt-4", "custom-model"],
            default_model="gpt-3.5-turbo",
            api_key_placeholder="sk-xxx或YOUR_API_KEY",
            base_url="https://api.openai.com/v1"
        )
    ]
    return providers


@router.post("/configure-llm")
async def configure_llm(config_req: LLMConfigRequest):
    """配置大模型"""
    try:
        # 验证提供商
        if config_req.provider not in [p.value for p in LLMProvider]:
            raise HTTPException(status_code=400, detail="不支持的大模型提供商")
        
        # 创建LLM配置
        config = LLMConfig(
            provider=LLMProvider(config_req.provider),
            api_key=config_req.api_key,
            model=config_req.model,
            base_url=config_req.base_url
        )
        
        # 配置LLM
        config_id = llm_service.configure_llm(config)
        
        return {
            "config_id": config_id,
            "message": "大模型配置成功",
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置大模型失败: {str(e)}")


@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """上传文档文件"""
    try:
        # 检查文件类型
        allowed_extensions = {'.txt', '.md', '.docx', '.xlsx', '.html', '.json'}
        file_extension = Path(file.filename).suffix.lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件类型: {file_extension}. 支持的类型: {', '.join(allowed_extensions)}"
            )
        
        # 生成唯一文件名
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_extension}"
        file_path = UPLOAD_DIR / filename
        
        # 保存文件
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
        
        # 解析文档
        parsed_doc = await document_parser.parse_document(str(file_path), file_extension)
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "file_type": file_extension,
            "file_size": len(content),
            "parsed_info": {
                "type": parsed_doc.get("type"),
                "metadata": parsed_doc.get("metadata", {}),
                "error": parsed_doc.get("error")
            },
            "message": "文件上传成功",
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.get("/analyze-document")
async def analyze_document(
    config_id: str,
    file_id: str,
    file_type: str
):
    """分析文档并流式返回API接口"""
    try:
        # 检查文件是否存在
        file_path = UPLOAD_DIR / f"{file_id}.{file_type.lstrip('.')}"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 解析文档内容
        parsed_doc = await document_parser.parse_document(str(file_path))
        
        if "error" in parsed_doc:
            raise HTTPException(status_code=400, detail=parsed_doc["error"])
        
        # 流式响应函数
        async def generate_analysis():
            try:
                # 发送开始消息
                yield f"data: {json.dumps({'type': 'start', 'message': '开始分析文档...', 'status': 'processing'}, ensure_ascii=False)}\n\n"
                
                # 分析文档
                async for result in llm_service.analyze_api_document(
                    config_id,
                    parsed_doc["content"],
                    parsed_doc["type"]
                ):
                    yield f"data: {json.dumps(result, ensure_ascii=False)}\n\n"
                
                # 发送完成消息
                yield f"data: {json.dumps({'type': 'complete', 'message': '文档分析完成', 'status': 'success'}, ensure_ascii=False)}\n\n"
                
            except Exception as e:
                # 发送错误消息
                error_msg = {
                    "type": "error",
                    "message": f"分析过程中出错: {str(e)}",
                    "status": "error"
                }
                yield f"data: {json.dumps(error_msg, ensure_ascii=False)}\n\n"
        
        return StreamingResponse(
            generate_analysis(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分析文档失败: {str(e)}")


@router.post("/save-apis")
async def save_apis(
    project_id: int = Form(...),
    apis_data: str = Form(...),
    db: Session = Depends(get_db)
):
    """保存解析出的API接口到数据库"""
    try:
        # 检查项目是否存在
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")
        
        # 解析API数据
        try:
            apis = json.loads(apis_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="API数据格式错误")
        
        # 保存API到数据库
        saved_apis = []
        for api_data in apis:
            # 创建API记录
            api = API(
                project_id=project_id,
                name=api_data.get("name", ""),
                description=api_data.get("description", ""),
                method=api_data.get("method", "GET"),
                path=api_data.get("path", ""),
                url=api_data.get("path", ""),  # 兼容旧字段
                tags=json.dumps(api_data.get("tags", []), ensure_ascii=False),
                parameters=json.dumps(api_data.get("parameters", []), ensure_ascii=False),
                responses=json.dumps(api_data.get("responses", []), ensure_ascii=False),
                security=json.dumps(api_data.get("security", []), ensure_ascii=False),
                notes=api_data.get("notes", "")
            )
            
            db.add(api)
            saved_apis.append(api)
        
        db.commit()
        
        return {
            "message": f"成功保存 {len(saved_apis)} 个API接口",
            "count": len(saved_apis),
            "status": "success"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"保存API失败: {str(e)}")


@router.delete("/cleanup-file/{file_id}")
async def cleanup_file(file_id: str):
    """清理上传的文件"""
    try:
        # 查找并删除文件
        for file_path in UPLOAD_DIR.glob(f"{file_id}.*"):
            file_path.unlink()
        
        return {
            "message": "文件清理成功",
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件清理失败: {str(e)}") 