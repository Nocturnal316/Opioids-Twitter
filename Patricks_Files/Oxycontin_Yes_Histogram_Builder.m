Tweets = importdata('Oxycontin_Yes_Histogram.txt');
Users = unique(Tweets);
% Numb = length(Users);
% Bins = Numb*100000;
% 
% [User_Tweets,User_Tweets_Cent] = hist(Tweets,Bins);

% subplot(2,1,1)
% semilogy(User_Tweets_Cent,User_Tweets,'o')
% title('Oxycontin Tweets by User Histogram')
% xlabel('User Twitter ID')
% ylabel('Number of Flagged Tweets')
% subplot(2,1,2)

% loglog(User_Tweets_Cent,User_Tweets,'o')
% title('Oxycontin Tweets by User Histogram')
% xlabel('User Twitter ID')
% ylabel('Number of Flagged Tweets')
% hold
% figure

temp = 0;
for i = 1:length(Users)
    for j = 1:length(Tweets)
       if Tweets(j,1) == Users(i,1)
           temp = temp + 1;
       end
    end
    Users(i,2) = temp;
    temp = 0;
end

width = [1:1:max(Users(:,2))];
[User_Tweets,User_Tweets_Cent] = hist(Users(:,2),max(Users(:,2)));
%User_Tweets_Cent = User_Tweets_Cent +0.5;
loglog(User_Tweets_Cent,User_Tweets,'o')
%bar(User_Tweets_Cent,User_Tweets)
title('Oxycontin Tweets by User Histogram')
xlabel('Number of Flagged Tweets')
ylabel('Number of Twitterers')
%set(gca,'YScale','log')
hold

% hold

% hold
% plot(User_Tweets_Cent,User_Tweets,'o')
% title('Oxycontin Tweets by User Histogram')
% xlabel('User')
% ylabel('Tweets')
% figure
% semilogy(User_Tweets_Cent,User_Tweets,'o')
% title('Oxycontin Tweets by User Histogram')
% xlabel('User')
% ylabel('Tweets')
% figure
% loglog(User_Tweets_Cent,User_Tweets,'o')
% title('Oxycontin Tweets by User Histogram')
% xlabel('User')
% ylabel('Tweets')