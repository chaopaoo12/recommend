# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 11:16:04 2015

@author: Administrator
"""

import ItemBase as IB
import UserBase as UB
import LoadData as LD
import Evaluate as EV
import LFM
from Preprocess import SplitData
  
#long running   
 
if __name__ == '__main__':
    work = 'Tag'
    if work == 'Movie': 
        data_path = 'G:\\pyhton\\recommended system\\dataset\\MovieLens'
        data = LD.LoadData(data_path)
        files = ['users','movies','ratings']
        names = [['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'],
                 ['MovieID', 'Title', 'Genres'],
                 ['UserID','MovieID','Rating','Timestamp']]
        splitmark = '::'
        [Movies, Users, Ratings] = data.getData(files = files, splitmark = splitmark, names = names)
        train, test = SplitData(Ratings, ['UserID','MovieID','Rating'], [0,1,2], 10, 1)
        ItemReco = IB.ItemBase(train)
        ItemReco = ItemReco.setMethod()
        ItemRank = ItemReco.Recommendation('5989',10)
        UserReco = UB.UserBase(train)
        UserReco = UserReco.setMethod()
        UserRank = UserReco.Recommendation('5989',10)
        Eva = EV.Evaluate(test)
        UserEva = Eva.setParam(UserReco)
        UserEva = UserEva.result(10)
        ItemEva = Eva.setParam(ItemReco)
        ItemEva = ItemEva.result(10)
        LFM = LFM.LFM(train)
        LFM = LFM.item_popularity()
        LFM = LFM.LatentFactorModel()
        LFMRank = LFM.Recommendation('5989')
    elif work == 'Tag':
        # tag
        data_path = 'G:\\pyhton\\recommended system\\dataset\\Delicious'
        files1 = ['bookmark_tags','bookmarks','tags',
                 'user_contacts','user_contacts-timestamps',
                 'user_taggedbookmarks','user_taggedbookmarks-timestamps']
        data = LD.LoadData(data_path)
        splitmark, names = None, None
        [user_taggedbookmarks, user_contacts_timestamps, 
         user_taggedbookmarks_timestamps, bookmarks,
         bookmark_tags, user_contacts, tags] = data.getData(files = files1, splitmark = splitmark, names  = names, sep = '\t')
        mark_index = ['userID', 'bookmarkID', 'tagID']
        train, test = SplitData(user_taggedbookmarks_timestamps, mark_index, [0,1,2], 10, 1)