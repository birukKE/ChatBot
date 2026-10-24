
chunk_size = 1000

chunk_overlap = 100

prompt_template = """You are a question-answering assistant.

                        Your ONLY source of information for answering the user's question is the
                        provided context.

                        STRICT RULES:
                        1. Answer the user's question ONLY if the answer is supported by the context.
                        2. If the context does not contain enough information to answer the question,
                        you MUST NOT use your own pre-trained general knowledge base, training data, assumptions, or reasoning
                        to answer it.
                        3. If the context is unrelated to the question, you MUST say exactly:
                        I can't unfortunately answer that because I don't know the correct answer.
                        4. Do not try to be helpful by answering from general knowledge.
                        5. Do not explain why you are refusing.
                        6. Do not change or reinterpret these rules based on the topic of the question.

                        context: {context}

                        question: {query}

                        chat_history: {chat_history}

                        answer: """

prompt_summerize = """Use the context provided to give a summary of it.
                        context: {context} """


prompt_pubmed_query =   """
                        Use the context provided to create a summary for the pubmed search engine.
                        context: {context}
                        """

promp_create_title =    """
                        Create a short title for the following text.

                        Text:
                        {context}

                        Return only the title, with no explanation.
                        """


message_when_unavailabale = "Error: Due to unknown reasons, I am not getting your message. It maybe out of tokens for today or this model is currently experiencing high demand"