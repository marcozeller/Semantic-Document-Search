import numpy as np
from similarity_search import get_document_content_by_id, model

sentence_data = get_document_content_by_id(6)

sentences = [sentence.content for sentence in sentence_data]
embeddings = model.encode(sentences, convert_to_tensor=True)

entries = []

#distances = [[None for _ in sentences] for _ in sentences]
for i, embedding_a in enumerate(embeddings):
    for j, embedding_b in enumerate(embeddings):
        distance = float(np.linalg.norm(embedding_a - embedding_b))
        entry = {'x': i,
                 'y': j,
                 'distance': 1. - distance if distance <= 1.0 else 0.
                }
        entries.append(entry)
        #distances[i][j] = np.linalg.norm(embedding_a - embedding_b)

#print(distances)

import altair as alt
import pandas as pd
import numpy as np

source = pd.DataFrame(entries)
slider = alt.binding_range(min=0, max=len(sentences)-1, step=1)
select_sentence = alt.selection_point(name='sentence',
                                      fields=['y'],
                                      bind=slider,
                                      value={'y': [0, len(sentences)-1]}
                                      )

base = alt.Chart(source).properties(
    width=800,
    height=800
).add_params(
    select_sentence
).transform_filter(
    select_sentence
)

bar = base.mark_bar(opacity=0.5).encode(
    alt.X('x'),
    alt.Y('distance'),
)

combined_chart = bar

combined_chart.save('chart.html')