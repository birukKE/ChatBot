# import torch

# DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

chunk_size = 1000

chunk_overlap = 100

prompt_template = """Use the context provided to answer 
                        the user's question below. If you do not know the answer 
                        based on the context provided, say exactly 
                        I can't unfortunately answer that because I don't know the correct answer.

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