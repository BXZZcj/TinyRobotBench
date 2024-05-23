keyword_prompt = "###\n" \
                 "请提取句子中的关键词, 按如下格式输出, 注意答案的开头为\"关键词: \". Let's think step by step.\n" \
                 "关键词: <逗号分隔的关键词列表>\n" \
                 "###\n" \
                 "下面是两个具体的例子: \n" \
                 "####\n" \
                 "例子1: \n" \
                 "句子: Logstash数据如何转发到外部UDP/TCP端口\n" \
                 "关键词: Logstash数据, 外部UDP/TCP端口\n" \
                 "####\n" \
                 "例子2: \n" \
                 "句子: 自定义菜单配置后,点击菜单,出现登录页面\n" \
                 "关键词: 自定义菜单, 点击, 登录页面\n" \
                 "###\n" \
                 "目标句子: "


def get_ticket_prompt(knowledge_list, user_question):
    ticket_prompt = "###\n" \
                    "知识: \n"
    for knowledge in knowledge_list:
        ticket_prompt += f'{knowledge} \n'

    ticket_prompt += "###\n" \
                     "请根据上述知识按如下格式尽可能详细回答问题. 让我们一步一步思考.\n" \
                     "答案: <逗号分隔的可能解决方案>\n" \
                     "###\n" \
                     f"目标问题: {user_question}\n"
    return ticket_prompt
