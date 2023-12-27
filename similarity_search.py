from sentence_transformers import SentenceTransformer
from torch import dist, flatten
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_test_texts():
    # https://en.wikipedia.org/wiki/Language_model
    document1 = "Wikipedia Language Model"

    test_text1 = """
    A language model is a probabilistic model of a natural language.[1] In 1980, the first significant statistical language model was proposed, and during the decade IBM performed ‘Shannon-style’ experiments, in which potential sources for language modeling improvement were identified by observing and analyzing the performance of human subjects in predicting or correcting text.[2]
    Language models are useful for a variety of tasks, including speech recognition[3] (helping prevent predictions of low-probability (e.g. nonsense) sequences), machine translation,[4] natural language generation (generating more human-like text), optical character recognition, handwriting recognition,[5] grammar induction,[6] and information retrieval.[7][8]
    Large language models, currently their most advanced form, are a combination of larger datasets (frequently using scraped words from the public internet), feedforward neural networks, and transformers. They have superseded recurrent neural network-based models, which had previously superseded the pure statistical models, such as word n-gram language model|. "
    """

    # https://en.wikipedia.org/wiki/Fox
    document2 = "Wikipedia Fox"

    test_text2 = """
    Foxes are small to medium-sized, omnivorous mammals belonging to several genera of the family Canidae. They have a flattened skull, upright, triangular ears, a pointed, slightly upturned snout, and a long bushy tail ("brush").
    Twelve species belong to the monophyletic "true fox" group of genus Vulpes. Approximately another 25 current or extinct species are always or sometimes called foxes; these foxes are either part of the paraphyletic group of the South American foxes, or of the outlying group, which consists of the bat-eared fox, gray fox, and island fox.[1]
    Foxes live on every continent except Antarctica. The most common and widespread species of fox is the red fox (Vulpes vulpes) with about 47 recognized subspecies.[2] The global distribution of foxes, together with their widespread reputation for cunning, has contributed to their prominence in popular culture and folklore in many societies around the world. The hunting of foxes with packs of hounds, long an established pursuit in Europe, especially in the British Isles, was exported by European settlers to various parts of the New World.
    """

    # https://en.wikipedia.org/wiki/Lorem_ipsum
    document3 = "Wikipedia Lorem Ipsum"

    test_text3 = """
    A common form of Lorem ipsum reads:
    Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """

    # https://en.wikipedia.org/wiki/Mountain
    document4 = "Mountain"

    test_text4 = """
    A mountain is an elevated portion of the Earth's crust, generally with steep sides that show significant exposed bedrock. Although definitions vary, a mountain may differ from a plateau in having a limited summit area, and is usually higher than a hill, typically rising at least 300 metres (980 ft) above the surrounding land. A few mountains are isolated summits, but most occur in mountain ranges.[1]
    Mountains are formed through tectonic forces, erosion, or volcanism,[1] which act on time scales of up to tens of millions of years.[2] Once mountain building ceases, mountains are slowly leveled through the action of weathering, through slumping and other forms of mass wasting, as well as through erosion by rivers and glaciers.[3]
    High elevations on mountains produce colder climates than at sea level at similar latitude. These colder climates strongly affect the ecosystems of mountains: different elevations have different plants and animals. Because of the less hospitable terrain and climate, mountains tend to be used less for agriculture and more for resource extraction, such as mining and logging, along with recreation, such as mountain climbing and skiing.
    The highest mountain on Earth is Mount Everest in the Himalayas of Asia, whose summit is 8,850 m (29,035 ft) above mean sea level. The highest known mountain on any planet in the Solar System is Olympus Mons on Mars at 21,171 m (69,459 ft).
    """

    documents = [document1, document2, document3, document4]
    texts = [test_text1, test_text2, test_text3, test_text4]

    return documents, texts

def clean_texts(documents, texts):
    # Clean texts
    for i in range(len(documents)):
        text = texts[i]
        # replace new line with space
        text = text.replace('\n', ' ')
        # replace multiple spaces with one space
        text = ' '.join(text.split())
        # reassemble splitted words
        text = text.replace('- ', '')

        texts[i] = text
    
    return texts

# Some global state will be moved into a database at some point
documents, texts = get_test_texts()
texts = clean_texts(documents, texts)
   
def get_similar_sentences(target_sentence, num_results=10):
    final_sentences = []
    final_docs = []
    final_sentence_numbers = []

    for doc, text in zip(documents, texts):
        sentences = text.split(".")
        for sentence_number, sentence in enumerate(sentences):
            if len(sentence) > 10:
                final_sentences.append(sentence)
                final_docs.append(doc)
                final_sentence_numbers.append(sentence_number)
    
    final_sentences.append(target_sentence)
    final_embeddings = model.encode(final_sentences, convert_to_tensor=True)
    target_embedding = flatten(final_embeddings[-1])

    final_corpus = [{'sentence_content': sentence,
                     'document': doc,
                     'sentence_number': sentence_number,
                     'distance': float(dist(flatten(embedding), target_embedding))}
                     for sentence, doc, sentence_number, embedding
                     in zip(final_sentences, final_docs, final_sentence_numbers, final_embeddings)] 


    final_corpus.sort(key=lambda x: x["distance"], reverse=False)

    return final_corpus[:num_results]

if __name__ == "__main__":
    test_sentence = "The fox is a lovely animal."
    print(get_similar_sentences(test_sentence, 3))

