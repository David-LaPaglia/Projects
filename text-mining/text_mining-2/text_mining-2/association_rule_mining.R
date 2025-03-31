install.packages("arules")
library(arules)

# Assuming your data frame is called `data`
# First, remove the non-feature columns

data <- read.csv("data/corpus_df_reddit.csv")


# Remove non-feature columns
features <- data[, !(names(data) %in% c("Review", "Label"))]

# Ensure binary (0/1) format
features[features > 1] <- 1

# Remove columns with only one unique value
features <- features[, sapply(features, function(x) length(unique(x)) > 1)]

# Convert to transactions
trans <- as(features, "transactions")

# Run Apriori algorithm
rules <- apriori(trans, parameter = list(supp = 0.01, conf = 0.5, maxlen=2))

# Top 15 by support
top_support <- sort(rules, by = "support", decreasing = TRUE)[1:15]

# Top 15 by confidence
top_confidence <- sort(rules, by = "confidence", decreasing = TRUE)[1:15]

# Top 15 by lift
top_lift <- sort(rules, by = "lift", decreasing = TRUE)[1:15]
inspect(top_support)
inspect(top_confidence)
inspect(top_lift)


# Plot
# Plot top 15 by support
plot(top_support, method = "graph", engine = "htmlwidget")

# Plot top 15 by confidence
plot(top_confidence, method = "graph", engine = "htmlwidget")

# Plot top 15 by lift
plot(top_lift, method = "graph", engine = "htmlwidget")



library(arulesViz)
plot(rules, method = "graph", engine = "htmlwidget")
