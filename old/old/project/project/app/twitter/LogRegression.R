
TwitterLRData <- read.csv("FinalDS_AdditionalFeatures.csv",header=T,stringsAsFactors = FALSE)
View(TwitterLRData)

library(aod)
library(ggplot2)

attach(TwitterLRData)
#detach(TwitterLRData)
sapply(TwitterLRData, class)

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
                                                      no_of_words,
                                                      Final.Label))

print("1")
print("2")
#TwitterSubsetLRData$Label <- as.factor(TwitterSubsetLRData$Label)

View(TwitterSubsetLRData)
samp_size <- floor(0.80 * nrow(TwitterSubsetLRData))
set.seed(2345)

#Converting character class to factors
TwitterSubsetLRData$user_has_url. <- as.factor(TwitterSubsetLRData$user_has_url.)
TwitterSubsetLRData$user_verified <- as.factor(TwitterSubsetLRData$user_verified)
TwitterSubsetLRData$Final.Label <- as.factor(TwitterSubsetLRData$Final.Label)
#TwitterSubsetLRData$polarity <- as.factor(TwitterSubsetLRData$polarity)
#TwitterSubsetLRData$Source_Category <- as.factor(TwitterSubsetLRData$Source_Category)

sapply(TwitterSubsetLRData, class)

tweet_ind <- sample(seq_len(nrow(TwitterSubsetLRData)), size = samp_size)
tweet_trainLR <- TwitterSubsetLRData[tweet_ind,]
tweet_testLR <- TwitterSubsetLRData[-tweet_ind,]

prop.table(table(tweet_trainLR$Final.Label))
prop.table(table(tweet_testLR$Final.Label))


logRegModel <- glm(Final.Label~ retweet_count+
                     favorite_count+ length +
                     user_statuses_count
                     + user_verified
                     + user_has_url.
                     + user_friends_count
                     + user_statuses_count
                     + user_followers_count
                     + no_of_question_marks
                     + no_of_exclamation_marks
                     + no_of_colon_marks
                     + no_of_hashtags + no_of_mentions
                     + no_of_urls + no_of_words ,
                     #+ no_of_firstOrderPronoun + no_of_secondOrderPronoun
                     #+ no_of_thirdOrderPronoun + Age_of_UserAccount_indays,
                     data = tweet_trainLR,
                     family = binomial)

#logRegModel
summary(logRegModel)

View(tweet_trainLR)
View(tweet_testLR)
tweet_testLR$predict_label <- c(1:nrow(tweet_testLR))
tweet_testLR$predict_label <- NA
tweet_testLR$predict_label <- predict(logRegModel, newdata=tweet_testLR, type="response")

tweet_testLR$predict_final_label <- c(1:nrow(tweet_testLR))
tweet_testLR$predict_final_label <- ifelse(tweet_testLR$predict_label > 0.5, 1,0)



save(logRegModel, file = "my_model1.rda")
print("-----------------")
#saveRDS(logRegModel, file = "model.sav")
print("3")
print(tweet_testLR[0:2])