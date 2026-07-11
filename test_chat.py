from src.rag import RAGChatbot

bot = RAGChatbot()

while True:
    question = input("\nAsk a question (type 'exit' to quit): ")

    if question.lower() == "exit":
        break

    answer = bot.ask(question)

    print("\nAnswer:")
    print(answer)