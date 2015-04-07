list.of.packages <- c("ggplot2", "dplyr")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)

library(ggplot2)
library(dplyr)

graph <- function() {
  res = read.csv("results.csv", header=FALSE)
  res = mutate(res, Percent = 100*(V2/(sum(res$V2))))
  
  if (nrow(res) >= 10){
    res = head(res,10)
  }
  
  p = ggplot(data=res, aes(x=V1, y=V2, fill=Percent)) + geom_bar(stat="identity") + coord_flip() + xlab('State') + ylab('Total Violations')
  ggsave(file="country_graph.pdf")
}
graph()
