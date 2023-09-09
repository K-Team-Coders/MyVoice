from sklearn.cluster import MiniBatchKMeans,KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import re


def mbkmeans_clusters(X, k,  print_silhouette_values=False):

    km = KMeans(n_clusters=k).fit(X)
    print(f"For n_clusters = {k}")
    print(f"Silhouette coefficient: {silhouette_score(X, km.labels_):0.2f}")
    print(f"Inertia:{km.inertia_}")

    sample_silhouette_values = silhouette_samples(X, km.labels_)
    print(f"Silhouette values:")
    silhouette_values = []

    for i in range(k):
        cluster_silhouette_values = sample_silhouette_values[km.labels_ == i]
        silhouette_values.append(
            (
                i,
                cluster_silhouette_values.shape[0],
                cluster_silhouette_values.mean(),
                cluster_silhouette_values.min(),
                cluster_silhouette_values.max(),
            )
        )
    silhouette_values = sorted(
        silhouette_values, key=lambda tup: tup[2], reverse=True
    )

    for s in silhouette_values:
        print(
            f"    Cluster {s[0]}: Size:{s[1]} | Avg:{s[2]:.2f} | Min:{s[3]:.2f} | Max: {s[4]:.2f}"
        )
    return {"silhoute_all":silhouette_score(X, km.labels_),"Inertia_all":km.inertia_,"silhoute_per_cluster":silhouette_values}

def censor_text(text, censored_words):
    
    # Создаем регулярное выражение для поиска нецензурных слов
    censored_pattern = r"\b(" + "|".join(re.escape(word) for word in censored_words) + r")\b"

    # Заменяем нецензурные слова на звездочки
    censored_text = re.sub(censored_pattern, lambda x: "*" * len(x.group()), text, flags=re.IGNORECASE)

    return censored_text