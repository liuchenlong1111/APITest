<template>
  <div class="dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="24" class="mb-24">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalProjects }}</div>
            <div class="stat-label">项目总数</div>
          </div>
          <div class="stat-icon project-icon">
            <el-icon><Folder /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalApis }}</div>
            <div class="stat-label">接口总数</div>
          </div>
          <div class="stat-icon api-icon">
            <el-icon><Connection /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.totalTests }}</div>
            <div class="stat-label">测试总数</div>
          </div>
          <div class="stat-icon test-icon">
            <el-icon><Operation /></el-icon>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-number">{{ stats.successRate }}%</div>
            <div class="stat-label">成功率</div>
          </div>
          <div class="stat-icon success-icon">
            <el-icon><TrendCharts /></el-icon>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24">
      <!-- 测试趋势图表 -->
      <el-col :span="16">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span>测试趋势</span>
              <el-radio-group v-model="chartPeriod" size="small">
                <el-radio-button label="7d">最近7天</el-radio-button>
                <el-radio-button label="30d">最近30天</el-radio-button>
              </el-radio-group>
            </div>
          </template>
          <div ref="trendChart" class="chart-container"></div>
        </el-card>
      </el-col>

      <!-- 最近活动 -->
      <el-col :span="8">
        <el-card class="activity-card">
          <template #header>
            <span>最近活动</span>
          </template>
          <div class="activity-list">
            <div
              v-for="activity in recentActivities"
              :key="activity.id"
              class="activity-item"
            >
              <div class="activity-avatar">
                <el-icon>
                  <component :is="getActivityIcon(activity.type)" />
                </el-icon>
              </div>
              <div class="activity-content">
                <div class="activity-text">{{ activity.description }}</div>
                <div class="activity-time">{{ formatTime(activity.createdAt) }}</div>
              </div>
            </div>
            <div v-if="recentActivities.length === 0" class="empty-activity">
              暂无活动记录
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" class="mt-24">
      <!-- 项目列表 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>我的项目</span>
              <el-button type="primary" size="small" @click="$router.push('/projects')">
                查看全部
              </el-button>
            </div>
          </template>
          <div class="project-list">
            <div
              v-for="project in recentProjects"
              :key="project.id"
              class="project-item"
              @click="$router.push(`/projects/${project.id}`)"
            >
              <div class="project-info">
                <div class="project-name">{{ project.name }}</div>
                <div class="project-desc">{{ project.description }}</div>
              </div>
              <div class="project-stats">
                <el-tag size="small">{{ project.apiCount }} 个接口</el-tag>
              </div>
            </div>
            <div v-if="recentProjects.length === 0" class="empty-projects">
              暂无项目
            </div>
          </div>
        </el-card>
      </el-col>

      <!-- 快速操作 -->
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快速操作</span>
          </template>
          <div class="quick-actions">
            <el-button
              type="primary"
              size="large"
              class="action-button"
              @click="$router.push('/projects')"
            >
              <el-icon><Plus /></el-icon>
              创建项目
            </el-button>
            <el-button
              type="success"
              size="large"
              class="action-button"
              @click="$router.push('/apis')"
            >
              <el-icon><Connection /></el-icon>
              管理接口
            </el-button>
            <el-button
              type="warning"
              size="large"
              class="action-button"
              @click="$router.push('/scenarios')"
            >
              <el-icon><Operation /></el-icon>
              场景测试
            </el-button>
            <el-button
              type="info"
              size="large"
              class="action-button"
              @click="$router.push('/reports')"
            >
              <el-icon><DataAnalysis /></el-icon>
              查看报告
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import dayjs from 'dayjs'
import {
  Folder,
  Connection,
  Operation,
  TrendCharts,
  Plus,
  DataAnalysis,
  Edit,
  Check,
  Warning
} from '@element-plus/icons-vue'

// 响应式数据
const trendChart = ref<HTMLElement>()
const chartPeriod = ref('7d')
let chartInstance: echarts.ECharts | null = null

const stats = reactive({
  totalProjects: 5,
  totalApis: 48,
  totalTests: 126,
  successRate: 92
})

const recentActivities = ref([
  {
    id: 1,
    type: 'test',
    description: '执行了 "用户登录流程" 场景测试',
    createdAt: new Date(Date.now() - 2 * 60 * 1000)
  },
  {
    id: 2,
    type: 'api',
    description: '添加了新接口 "获取用户信息"',
    createdAt: new Date(Date.now() - 15 * 60 * 1000)
  },
  {
    id: 3,
    type: 'project',
    description: '创建了新项目 "电商平台API"',
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000)
  }
])

const recentProjects = ref([
  {
    id: 1,
    name: '用户管理系统',
    description: '用户认证和权限管理相关接口',
    apiCount: 12
  },
  {
    id: 2,
    name: '订单管理系统',
    description: '订单创建、查询、更新等接口',
    apiCount: 18
  },
  {
    id: 3,
    name: '支付系统',
    description: '支付、退款、查询等接口',
    apiCount: 8
  }
])

// 初始化图表
const initChart = () => {
  if (!trendChart.value) return

  chartInstance = echarts.init(trendChart.value)
  
  const option = {
    title: {
      text: '测试执行趋势',
      textStyle: {
        fontSize: 14,
        fontWeight: 'normal'
      }
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['成功', '失败']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: generateDateRange()
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '成功',
        type: 'line',
        smooth: true,
        data: [12, 15, 18, 22, 19, 25, 28],
        itemStyle: {
          color: '#67c23a'
        }
      },
      {
        name: '失败',
        type: 'line',
        smooth: true,
        data: [2, 3, 1, 4, 2, 3, 2],
        itemStyle: {
          color: '#f56c6c'
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

// 生成日期范围
const generateDateRange = () => {
  const days = chartPeriod.value === '7d' ? 7 : 30
  const dates = []
  for (let i = days - 1; i >= 0; i--) {
    dates.push(dayjs().subtract(i, 'day').format('MM-DD'))
  }
  return dates
}

// 获取活动图标
const getActivityIcon = (type: string) => {
  const icons = {
    test: Operation,
    api: Connection,
    project: Folder,
    success: Check,
    error: Warning
  }
  return icons[type as keyof typeof icons] || Edit
}

// 格式化时间
const formatTime = (date: Date) => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 60 * 1000) {
    return '刚刚'
  } else if (diff < 60 * 60 * 1000) {
    return `${Math.floor(diff / (60 * 1000))} 分钟前`
  } else if (diff < 24 * 60 * 60 * 1000) {
    return `${Math.floor(diff / (60 * 60 * 1000))} 小时前`
  } else {
    return dayjs(date).format('MM-DD HH:mm')
  }
}

// 监听图表周期变化
const handleChartPeriodChange = () => {
  if (chartInstance) {
    const option = chartInstance.getOption() as any
    option.xAxis[0].data = generateDateRange()
    chartInstance.setOption(option)
  }
}

// 窗口大小调整
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

onMounted(() => {
  initChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  window.removeEventListener('resize', handleResize)
})

// 监听周期变化
watch(chartPeriod, handleChartPeriodChange)
</script>

<style lang="scss" scoped>
.dashboard {
  .stat-card {
    position: relative;
    overflow: hidden;

    .stat-content {
      .stat-number {
        font-size: 32px;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 8px;
      }

      .stat-label {
        color: #7f8c8d;
        font-size: 14px;
      }
    }

    .stat-icon {
      position: absolute;
      right: 20px;
      top: 50%;
      transform: translateY(-50%);
      font-size: 48px;
      opacity: 0.1;

      &.project-icon {
        color: #409eff;
      }

      &.api-icon {
        color: #67c23a;
      }

      &.test-icon {
        color: #e6a23c;
      }

      &.success-icon {
        color: #f56c6c;
      }
    }
  }

  .chart-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .chart-container {
      height: 300px;
      width: 100%;
    }
  }

  .activity-card {
    .activity-list {
      max-height: 300px;
      overflow-y: auto;
    }

    .activity-item {
      display: flex;
      align-items: flex-start;
      padding: 12px 0;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }

      .activity-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #f5f5f5;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 12px;
        flex-shrink: 0;

        .el-icon {
          font-size: 16px;
          color: #909399;
        }
      }

      .activity-content {
        flex: 1;

        .activity-text {
          font-size: 14px;
          color: #2c3e50;
          margin-bottom: 4px;
        }

        .activity-time {
          font-size: 12px;
          color: #909399;
        }
      }
    }

    .empty-activity {
      text-align: center;
      color: #909399;
      padding: 40px 0;
    }
  }

  .project-list {
    .project-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 0;
      border-bottom: 1px solid #f0f0f0;
      cursor: pointer;
      transition: background-color 0.3s;

      &:hover {
        background-color: #f8f9fa;
        margin: 0 -20px;
        padding: 16px 20px;
        border-radius: 8px;
      }

      &:last-child {
        border-bottom: none;
      }

      .project-info {
        .project-name {
          font-size: 16px;
          font-weight: 600;
          color: #2c3e50;
          margin-bottom: 4px;
        }

        .project-desc {
          font-size: 14px;
          color: #7f8c8d;
        }
      }
    }

    .empty-projects {
      text-align: center;
      color: #909399;
      padding: 40px 0;
    }
  }

  .quick-actions {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;

    .action-button {
      height: 60px;
      border-radius: 8px;
      font-size: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;

      .el-icon {
        margin-bottom: 4px;
        font-size: 20px;
      }
    }
  }
}

.mt-24 {
  margin-top: 24px;
}
</style> 