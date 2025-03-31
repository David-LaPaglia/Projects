# Load required packages
library(proxy)    # for cosine distance
library(cluster)  # for clustering
library(stats)    # hclust is in base R


getwd()
# Load full dataset
dtm_raw <- read.csv("data/corpus_df_reddit_processed.csv")

# Inspect structure to confirm column types
str(dtm_raw)

# Drop all non-numeric columns automatically (not just the first one)
dtm_clean <- dtm_raw[, sapply(dtm_raw, is.numeric)]

# Check for non-numeric values
str(dtm_clean)                # Should show only int or num
sum(is.na(dtm_clean))         # Should be 0

# Convert to matrix
dtm_matrix <- as.matrix(dtm_clean)

normalize <- function(m) {
  return(m / sqrt(rowSums(m^2)))
}

dtm_norm <- normalize(dtm_matrix)


# Compute cosine distance (1 - cosine similarity)
cosine_dist <- dist(dtm_norm, method = "cosine")

# Perform hierarchical clustering
hc <- hclust(cosine_dist, method = "ward.D2")  # or "average", "complete", etc.
labels <- dtm_raw$X  # This is your first column

# Plot with labels
plot(hc, labels = labels, main = "Hierarchical Clustering of Subreddits", xlab = "", sub = "", cex = 0.7)



hc$order                   # Index of documents in plotted order
labels[hc$order]          # Subreddit names in dendrogram order


clusters <- cutree(hc, k = 4)  # Try 3, 4, 5, etc.
table(clusters)               # Count docs per cluster

# Combine with subreddit labels
result <- data.frame(Subreddit = labels, Cluster = clusters)
print(result)






library(ggplot2)
library(Rtsne)

# Perform t-SNE on normalized matrix
tsne <- Rtsne(dtm_norm, dims = 2, perplexity = 5, verbose = TRUE)

# Create dataframe for plotting
tsne_df <- data.frame(
  X = tsne$Y[,1],
  Y = tsne$Y[,2],
  Cluster = factor(clusters),
  Subreddit = labels
)

# Plot
ggplot(tsne_df, aes(x = X, y = Y, color = Cluster, label = Subreddit)) +
  geom_point(size = 3) +
  geom_text(size = 3, vjust = 1.5, check_overlap = TRUE) +
  labs(title = "t-SNE Visualization of Subreddits by Cluster") +
  theme_minimal()







###### Clustering more with Kmeans here!!!

library(cluster)
library(factoextra)  # for nice visualizations

# Normalize data if you haven’t already
normalize <- function(m) m / sqrt(rowSums(m^2))
dtm_norm <- normalize(dtm_matrix)

# Try several values of k
sil_scores <- c()
k_values <- 2:10

for (k in k_values) {
  km_result <- kmeans(dtm_norm, centers = k, nstart = 25)
  sil <- silhouette(km_result$cluster, dist(dtm_norm, method = "euclidean"))
  avg_sil <- mean(sil[, 3])  # Silhouette width
  sil_scores <- c(sil_scores, avg_sil)
}

library(ggplot2)

sil_df <- data.frame(K = k_values, Silhouette = sil_scores)

ggplot(sil_df, aes(x = K, y = Silhouette)) +
  geom_line(color = "steelblue") +
  geom_point(size = 3, color = "darkred") +
  labs(title = "Silhouette Scores for Different K Values",
       x = "Number of Clusters (K)",
       y = "Average Silhouette Width") +
  theme_minimal()
k_best <- 7  # or your selected value
km <- kmeans(dtm_norm, centers = k_best, nstart = 25)
table(km$cluster)


# Load package
library(akmeans)
install.packages('akmeans')
# Run adaptive k-means using cosine similarity (d.metric = 3)
ak_result <- akmeans(m, d.metric = 3, ths3 = 0.8, mode = 3)

# Check cluster assignments
ak_result$cluster

# Number of clusters found
length(unique(ak_result$cluster))
library(factoextra)

# Dimensionality reduction (PCA)
m_pca <- prcomp(m)
pca_df <- data.frame(m_pca$x[, 1:2], Cluster = factor(ak_result$cluster))

# Visualize
ggplot(pca_df, aes(x = PC1, y = PC2, color = Cluster)) +
  geom_point(size = 3) +
  labs(title = "Adaptive K-means Clustering (Cosine Distance via akmeans)") +
  theme_minimal()



library(factoextra)
install.packages("lsa")
library(lsa)   # For cosine()

# Compute cosine similarity, then convert to distance
cosine_sim <- cosine(t(dtm_matrix))     # cosine() expects documents as columns
cosine_dist <- 1 - cosine_sim

# Classical k-means doesn’t accept custom distance, but clustering can be applied via PAM
library(cluster)
pam_res <- pam(as.dist(cosine_dist), k = 7)

# Visualize
fviz_cluster(list(data = dtm_matrix, cluster = pam_res$clustering),
             main = "PAM Clustering with Cosine Distance")


