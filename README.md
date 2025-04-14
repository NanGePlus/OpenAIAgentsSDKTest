# 1、项目介绍
## 1.1、本次分享介绍    
主要内容:OpenAI Agents SDK基础功能测试,支持多种类型的大模型             
https://youtu.be/Ft5kiR8dx88         
https://www.bilibili.com/video/BV1n7QdY8Emf/             

## 1.2 介绍 
OpenAI 于 2025 年 3 月 11 日正式发布了开源的 OpenAI Agents SDK，这是一个专为构建智能代理（AI Agents）的轻量级且生产就绪的开发工具包                  
它是 OpenAI 此前实验性框架 Swarm 的升级版本，旨在帮助开发者更轻松地创建、编排和管理多代理系统                         
官方文档:https://openai.github.io/openai-agents-python/                   
GitHub地址:https://github.com/openai/openai-agents-python                   
Swarm框架介绍，可以参考如下项目:https://github.com/NanGePlus/SwarmTest            
OpenAI Agents SDK 的设计围绕几个核心概念展开，旨在提供简单但强大的构建模块，支持开发者创建复杂的代理工作流：              
**代理（Agent）**             
代理是一个由大语言模型（LLM）驱动的独立单元，配备特定的指令（instructions）和工具（tools），能够根据用户输入执行任务                    
代理不仅限于 OpenAI 模型，还支持其他符合 Chat Completions 格式的模型                                       
**工具调用（Tool Calling）**                          
代理可以通过调用外部工具（如 Python 函数）扩展功能，SDK 自动生成并验证工具的输入输出模式（使用 Pydantic）                     
Tools（工具）使用是Agent的必备技能之一，在Agents SDK中有三种类型的工具:                       
托管工具:OpenAI的云端工具，包括WebSearch（搜索），FileSearch（OpenAI的云端向量搜索）、ComputerTool（计算机任务），只能支持OpenAI模型                
函数工具:这是基本上所有Agent框架都会支持的类型，即遵循一定规范的自定义函数，可用来实现自定义逻辑                 
Agent工具:把一个Agent再包装成一个工具，这也为构建一个多Agent系统提供了基础                                 
**移交（Handoffs）**                  
代理之间可以根据任务需求相互移交工作，并传递上下文，确保多代理协作的无缝衔接                         
**循环管理（Agent Loop）**                       
SDK 内置了代理循环机制，自动处理工具调用和响应生成，简化多步骤任务的执行                
**护栏（Guardrails）**                        
支持输入和输出的验证，确保代理行为符合预期并提高安全性                           
                


# 2、前期准备工作
## 2.1 集成开发环境搭建  
anaconda提供python虚拟环境,pycharm提供集成开发环境                                              
**具体参考如下视频:**                        
【大模型应用开发-入门系列】03 集成开发环境搭建-开发前准备工作                         
https://youtu.be/KyfGduq5d7w                     
https://www.bilibili.com/video/BV1nvdpYCE33/                      

## 2.2 大模型LLM服务接口调用方案
(1)gpt大模型等国外大模型使用方案                  
国内无法直接访问，可以使用代理的方式，具体代理方案自己选择                        
这里推荐大家使用:https://nangeai.top/register?aff=Vxlp                        
(2)非gpt大模型方案 OneAPI方式或大模型厂商原生接口                                              
(3)本地开源大模型方案(Ollama方式)                                              
**具体参考如下视频:**                                           
【大模型应用开发-入门系列】04 大模型LLM服务接口调用方案                    
https://youtu.be/mTrgVllUl7Y               
https://www.bilibili.com/video/BV1BvduYKE75/                              
                

# 3、项目初始化
## 3.1 下载源码
GitHub或Gitee中下载工程文件到本地，下载地址如下：                
https://github.com/NanGePlus/OpenAIAgentsSDKTest                              
https://gitee.com/NanGePlus/OpenAIAgentsSDKTest                                  

## 3.2 构建项目
使用pycharm构建一个项目，为项目配置虚拟python环境              
项目名称：OpenAIAgentsSDKTest                                  
虚拟环境名称保持与项目名称一致                 

## 3.3 将相关代码拷贝到项目工程中           
直接将下载的文件夹中的文件拷贝到新建的项目目录中                      

## 3.4 安装项目依赖          
命令行终端中直接运行如下命令安装依赖                  
pip install openai-agents==0.0.4                      


# 4、项目测试
运行 python demo.py             
