#计算token
def count_message_tokens(message:list[dict])->int:
    total = 0
    for msg in message:
        content = msg.get("content", "")
        #
        total += len(content)//2
        #
        total+=4
    return total

