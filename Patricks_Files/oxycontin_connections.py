import networkx as nx
import json
import pickle


flagged_users_file = file("Hand_Flagged_Users.txt")
graph_data = file ("07-2015_social_graph.json")

flagged_users = set()
reciprocal_users = set()


line = flagged_users_file.readline()
while line != "":
    try:
        flagged_users.add(int(line))
        line = flagged_users_file.readline()
    except ValueError:
        pass
        line = flagged_users_file.readline()
flagged_users_file.close()

print "Number of Flagged Users"
print len(flagged_users)
 
count1 = 0
count2 = 0
count3 = 0
connected_users = set()
file = open("Oxycontin_Connections.txt",'w')
recips = open("Reciprocal_Oxy_Users.txt",'w')
pantry = open("Reciprocal_Oxy_Social_Graph.json",'w')
holding = set()
while True:
    line = graph_data.readline()
    if line == "":
        break
    try:
        j = json.loads(line)
        if int(j["user_id"]) in flagged_users:
            follower = set(j["follower_ids"]).intersection(flagged_users)
            following = flagged_users.intersection(set(j["friend_ids"]))

            for followers in follower:
                file.write(str(j["user_id"]))
                file.write(" ")
                file.write(str(followers))
                file.write("\n")
                connected_users.add(int(j["user_id"]))
                connected_users.add(int(followers))

            for friends in following:
                file.write(str(friends))
                file.write(" ")
                file.write(str(j["user_id"]))
                file.write("\n") 
                connected_users.add(int(j["user_id"])) 
                connected_users.add(int(friends))

            count1 = count1 + 1  

            mutual = set(j["follower_ids"]).intersection(set(j["friend_ids"]))
            temp = mutual.intersection(flagged_users)
            for newbs in temp:
                if int(newbs) and int(j["user_id"]) not in reciprocal_users:
                    reciprocal_users.add(int(newbs))
                    reciprocal_users.add(int(j["user_id"]))
                    recips.write(str(j["user_id"]))
                    recips.write(str(" "))
                    recips.write(str(newbs))
                    recips.write("\n")
                    count2 = count2 + 1

            if int(j["user_id"]) in reciprocal_users:         
                if int(j["user_id"]) not in holding:
                    json.dump(j,pantry)
                    holding.add(int(j["user_id"]))
                    pantry.write("\n")
                    count3 = count3 + 1
    except ValueError:
        pass
file.close()
recips.close()
pantry.close()        

#graph_data.close()

print "Number of Flagged Users in the Graph File"
print count1
print "Number of Flagged Users in the Graph File with Connections"
print len(connected_users)

# graph_data.seek(0)
# count = 0
# file = open("Reciprocal_Oxy_Users.txt",'w')
# while True:
#     line = graph_data.readline()
#     if line == "":
#         break
#     try:
#         j = json.loads(line)
#         if int(j["user_id"]) in flagged_users:
#             mutual = set(j["follower_ids"]).intersection(set(j["friend_ids"]))
#             temp = mutual.intersection(flagged_users)
#             for newbs in temp:
#                 if int(newbs) and int(j["user_id"]) not in reciprocal_users:
#                     reciprocal_users.add(int(newbs))
#                     reciprocal_users.add(int(newbs))
#                     file.write(str(j["user_id"]))
#                     file.write(str(" "))
#                     file.write(str(newbs))
#                     file.write("\n")
#                     count = count + 1
#     except ValueError:
#         pass
# file.close()        

print "Number of Reciprocal Oxy User-Pairs"
print count2

print "Between this many users:"
print len(reciprocal_users)

print "Of whom this many Users are in the Graph File"
print count3



recips = open("Reciprocal_Oxy_Users.txt",'r')
pantry = open("Reciprocal_Oxy_Social_Graph.json",'r')
file = open("Oxycontin_User_Social_Triangles.txt",'w')
equalateral = open("Oxycontin_User_Triangle_Thirds.txt",'w')
num = 0
a = set()
b = set()
count4 = 0
count5 = 0
#triangles = set()
while True:
    line = recips.readline()
    if line == "":
        break
    try:
        pair = set(line.split())
        pair = [int(x) for x in pair]
        pair = set(pair)
        #print pair
        pantry.seek(0)
        a = set()
        b = set()
        tris = set()
        while True:
            peep = pantry.readline()
            if peep == "":
                break
            try:    
                j = json.loads(peep)
                #print pair

                #temp = set(j["user_id"])
                #temp = [int(x) for x in temp]

                #print set(int(j["user_id"]))
                #overlap = pair.intersection(set(int(j["user_id"])))

                #overlap = pair.intersection(temp)
                #print pair
                #print temp
                #print overlap
                #for people in overlap:
                #print j["user_id"]
                if int(j["user_id"]) in pair:
                    if num == 0:
                        a = set(j["follower_ids"]).intersection(set(j["friend_ids"]))
                        #print a
                        num = 1
                    else:
                        b = set(j["follower_ids"]).intersection(set(j["friend_ids"]))
                        #print b
                        num = 0           
            except ValueError:
                pass
        #print a
        #print b
        tris = a.intersection(b)
        #print len(a)
        #print len(b)
        #print len(tris)
        if len(tris) > 0:
            count4 = count4 + 1
        for members in tris:
            for originals in pair:
                file.write(str(originals))
                file.write(str(" "))
            file.write(str(members))
            file.write(str("\n"))
            count5 = count5 + 1
            #triangles.add(int(members))
            equalateral.write(str(members))
            equalateral.write(str("\n"))
    except ValueError:
        pass

recips.close()
pantry.close()
file.close()
equalateral.close()

print "Of the Oxy-User Pairs, this many have Triangles:"
print count4
print "Totaling to this many Triangles:"
print count5


graph_data.seek(0)

#print len(triangles)


graph_data.close()