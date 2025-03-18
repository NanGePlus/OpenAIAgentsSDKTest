import asyncio
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, GuardrailFunctionOutput, InputGuardrail, function_tool
from openai import AsyncOpenAI
from pydantic import BaseModel



# 禁用追踪功能
set_tracing_disabled(disabled=True)

# 创建一个异步 OpenAI 客户端实例，配置 API 密钥和基础 URL
openai_client = AsyncOpenAI(
    api_key="sk-aR2Y17PuOKtS7l1H2qPbrKSKPswr047o6AMvCG6g3EfViPku",
    base_url="https://nangeai.top/v1"
)


# 定义一个 OpenAI 聊天模型，使用指定的模型和客户端
model = OpenAIChatCompletionsModel(
    model='gpt-4o-mini',
    openai_client=openai_client
)


# 定义一个 Pydantic 数据模型，结构化输出，用于检查输出是否与历史问题相关
class RetrieverOutput(BaseModel):
    is_history: bool
    reasoning: str


# 定义工具
@function_tool
def get_weather(city: str) -> str:
    return f"{city} 的天气是大晴天。"


# 创建一个护栏代理，用于检查用户输入是否与历史问题相关
guardrail_agent = Agent(
    name="Guardrail check",
    model=model,
    instructions="判断用户问题是不是关于历史的问题",
    output_type=RetrieverOutput
)


# 创建一个历史辅导代理，专门处理历史相关问题
history_tutor_agent = Agent(
    name="History Tutor",
    model=model,
    handoff_description="历史问题专家代理",
    instructions="你为历史查询提供帮助。清楚地解释重要事件和来龙去脉。"
)


# 创建一个天气查询代理，专门处理天气信息
weather_agent = Agent(
    name="Math Tutor",
    model=model,
    tools=[get_weather],
    handoff_description="天气查询专家代理",
    instructions="你借助工具为用户的天气问题提供帮助。"
)

# 定义一个异步护栏函数，用于在输入时检查是否与历史问题相关
async def retriever_guardrail(ctx, agent, input_data):
    # 运行护栏代理，检查输入内容
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    # 将运行结果转换为 RetrieverOutput 类型
    final_output = result.final_output_as(RetrieverOutput)
    print(f"final_output:{final_output}")
    # 返回护栏函数的输出，包含检查结果和是否触发限制的标志
    return GuardrailFunctionOutput(
        # 检查结果
        output_info=final_output,
        # 如果不是，则触发限制
        tripwire_triggered=not final_output.is_history,
    )


# 创建一个分诊代理，用于根据用户问题决定调用哪个代理
triage_agent = Agent(
    name="Triage Agent",
    model=model,
    instructions="根据用户的问题决定使用哪个代理",
    # 可移交的代理列表
    handoffs=[history_tutor_agent, weather_agent],
    # 输入护栏，调用上面定义的护栏函数
    input_guardrails=[
        InputGuardrail(guardrail_function=retriever_guardrail),
    ],
)


# 定义主异步函数，用于运行程序
async def main():
    # 测试1 运行分诊代理，处理历史问题
    result = await Runner.run(triage_agent, "一个历史问题，美国的第一任总统是谁?")
    print(result.final_output)

    # 测试2 运行分诊代理，处理天气查询
    # result = await Runner.run(triage_agent, "上海今天的天气如何？")
    # print(result.final_output)


# 判断是否为主程序入口，若是则运行 main 函数
if __name__ == "__main__":
    # 使用 asyncio 运行异步主函数
    asyncio.run(main())


