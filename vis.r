graph <- function() {
  res = read.csv("results.csv", header=FALSE)
  res = mutate(res, Percent = 100*(V2/(sum(res$V2))))
  
  if (nrow(res) >= 10){
    res = head(res,10)
  }
  
  p = ggplot(data=res, aes(x=V1, y=V2, fill=Percent)) + geom_bar(stat="identity") + coord_flip() + xlab('Facility') + ylab('Number Of Violations')
  ggsave(file="graph.pdf")
}
graph()
