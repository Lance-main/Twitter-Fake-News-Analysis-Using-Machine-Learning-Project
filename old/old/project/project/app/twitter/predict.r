




getPrediction<-function(filename,modelpath)
{


TwitterLRData <- read.csv(filename,header=T,stringsAsFactors = FALSE)


TwitterSubsetLRData <- subset(TwitterLRData, select=c(retweet_count, favorite_count,
                                                      length, user_statuses_count,
                                                      user_verified,
                                                      user_friends_count,
                                                      user_statuses_count,
                                                      user_followers_count,
                                                      user_has_url.,
                                                      no_of_question_marks,no_of_exclamation_marks,
                                                      no_of_hashtags, no_of_mentions,
                                                      no_of_urls,no_of_colon_marks,
                                                      no_of_words))









#tweet_testLR <- TwitterSubsetLRData[0:]







bar <- load(modelpath)
 #new.cars <- data.frame(wt=c(0,0,138,22625,"False",37.150000,1.410000000,"Yes",0,0,1,1,1,0,16))
p.int <- predict(get(bar),newdata=TwitterSubsetLRData , type="response")

line=p.int
write(line,file="output.txt")

predict_final_label <- ifelse(p.int > 0.5, 1,0)

print(predict_final_label)

return(p.int)
}

args = commandArgs(trailingOnly=TRUE)
getPrediction(args[1],args[2])