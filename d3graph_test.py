# Import library
from d3graph import d3graph, vec2adjmat
from similarity_search import get_documents_in_db, get_document_content_by_id, get_similar_sentences

color_selection = {0:  '#000000',
                   1:  '#FF0000',
                   2:  '#00FF00',
                   3:  '#0000FF',
                   4:  '#AA0000',
                   5:  '#00AA00',
                   6:  '#0000AA',
                   7:  '#880000',
                   8:  '#008800',
                   9:  '#000088',
                   10: '#440000',
                   11: '#004400',
                   12: '#000044',
                   13: '#220000',
                   }

documents = get_documents_in_db()
source = []
target = []
weight = []

node_labels = {}
doc_labels = {}

for doc in documents[:10]:
    sentences = get_document_content_by_id(doc.id)
    for sentence in sentences[200:220]:
        node_labels[str(sentence.id)] = sentence.content
        doc_labels[str(sentence.id)] = sentence.document_id
        similar_sentences = get_similar_sentences(sentence.content, 2)
        for sim_sentence in similar_sentences:
            if sentence.content == sim_sentence.content:
                continue
            node_labels[str(sim_sentence.id)] = sim_sentence.content 
            doc_labels[str(sim_sentence.id)] = sim_sentence.document_id
            source.append(str(sentence.id))
            target.append(str(sim_sentence.id))
            weight.append(1 / sim_sentence.distance)

#node_ids = list(node_labels.keys())
#node_ids.sort()


# Create example network
#source = ['node A','node F','node B','node B','node B','node A','node C','node Z']
#target = ['node F','node B','node J','node F','node F','node M','node M','node A']
#weight = [5.56, 0.5, 0.64, 0.23, 0.9, 3.28, 0.5, 0.45]
# Convert to adjacency matrix
adjmat = vec2adjmat(source, target, weight=weight)

# Initialize
d3 = d3graph()
# Proces adjmat
d3.graph(adjmat, )
# Plot
#d3.show()

# Build tooltip list accoording to adjaceny matrix order as this is the order expected by the library
node_ids = adjmat.index.values
tooltip = [f"{node_id}: {node_labels[node_id]}" for node_id in node_ids]
colors = [color_selection[doc_labels[node_id]] for node_id in node_ids]
labels = [f"{node_labels[node_id][:30]}..." for node_id in node_ids]
#print(colors)

#print(tooltip)
#print(adjmat)
#print(adjmat.columns.values)

# Make changes in node properties
d3.set_node_properties(label=labels, tooltip=tooltip, color=colors,)
# Plot
d3.show(filepath='d3graph_test.html')