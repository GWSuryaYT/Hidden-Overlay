class chunky:
    def __init__(self):
        pass

    def chunk_maker(self, paragraph:str, overlap:int, chunk_size:int):

        overlap = -overlap

        sentence_list = paragraph.split('.')

        chunked_text = ''

        all_chunks = []

        for sentence in sentence_list:

            words = len(sentence.split())

            if words < chunk_size:

                chunked_text = chunked_text + sentence + '.'

            else:

                all_chunks.append(chunked_text)

                #now start a new chunk from that.
                chunked_text = " ".join(chunked_text.split()[overlap:]) + sentence + '.'

        all_chunks.append(chunked_text)
        return all_chunks