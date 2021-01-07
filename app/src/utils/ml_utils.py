from typing import Set, List, Tuple
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from collections import Counter
import numpy as np
from iteration_utilities import deepflatten
import string
import datetime
import random
import requests
import json


from app.src.utils.geo import GeoParser
from app.config import MODEL_URL, SEARCH_LIMIT


def init_cache():
    global recEngine, idf_d, jobs, edu_d, empt_d
    from app.src.models.models import WordIdf, Job, EducationDegree, EmploymentType

    idf_d = WordIdf.as_dict()
    edu_d = EducationDegree.as_dict()
    empt_d = EmploymentType.as_dict()
    jobs = set(Job.query.filter_by(is_active=1))



class TxtParser:
    vectorizerIdf = TfidfVectorizer(use_idf=True)
    punct_table = str.maketrans('', '', string.punctuation)
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))


    @staticmethod
    def raw_txt(txt: str) -> str:
        """ Text preprocessing
        """
        # tokenize lower text
        if txt and type(txt) is str:
            txt = word_tokenize(txt.lower())

            # remove non alphabetic words and stop words and and remove punctuation
            txt = " ".join([word.translate(TxtParser.punct_table) for word in txt if word.isalpha()]).split()
            return " ".join([(TxtParser.stemmer.stem(w)) for w in txt if w not in TxtParser.stop_words and len(w) > 2])
        return ""


    @staticmethod
    def similiarity_ratio(tokA:Set[str], tokB:Set[str], word_diff:int = 2, ratio_bias:float = 0.75) -> int:
        """ Get similiarity between two lists of tokens (Overlap coefficient)
        """
        match_ctr = 0
        wrd_ctr = min(len(tokA), len(tokB))

        for w1 in tokA:
            for w2 in tokB:
                if abs(len(w1) - len(w2)) <= word_diff:
                    if TxtParser.str_ratio(w1, w2) > ratio_bias:
                        match_ctr += 1
        if wrd_ctr:
            return  match_ctr/wrd_ctr
        return random.uniform(0.00001, 0.05)


    @staticmethod
    def str_ratio(strA, strB):
        """ Ratio between two strings
        """
        return SequenceMatcher(None, strA, strB).ratio()


    @staticmethod
    def idf(txt: List[str]) -> List[Tuple[str, int]]:
        TxtParser.vectorizerIdf.fit_transform(txt)
        return list(zip(TxtParser.vectorizerIdf.get_feature_names(), TxtParser.vectorizerIdf.idf_))


    @staticmethod
    def tfidf(txt:List[str], threshold=0.06):
        wrd_ctr = Counter(txt)
        res = set()
        t_len = len(txt)

        for k, v in wrd_ctr.most_common():
            tfidf = 0
            if k in idf_d:
                tfidf = (v/t_len)*idf_d[k]
                if tfidf > threshold:
                    res.add(k)

        return res



class DataTools:

    @staticmethod
    def normalize(X):
        for rowx in X:
            rowx[3] /= 100
            rowx[4] /= 4
            rowx[5] /= 4
            rowx[6] /= 700
            if rowx[6] >= 1:
                rowx[6] = random.uniform(0.97, 0.9999999999)
        return X


    @staticmethod
    def nn_data_builder(job, empInt, empPos, empDesc, empAge, empCoord, keywords):
        c_split = lambda x : x.split() if type(x) is str else []

        jobEdu = job.education_required
        jobEtyp = job.employment_type
        jobCord = job.latitude, job.longitude
        jobDesc = list(c_split(job.desc_raw))
        jobPos = set(c_split(job.pos_raw))

        emptfidf = TxtParser.tfidf(empDesc).union(empInt)
        jobtfidf = TxtParser.tfidf(jobDesc).union(jobPos)

        return [
            TxtParser.similiarity_ratio(empInt.union(keywords), jobtfidf),
            TxtParser.similiarity_ratio(empPos.union(keywords), jobtfidf),
            TxtParser.similiarity_ratio(emptfidf.union(keywords), jobtfidf),
            empAge,
            jobEdu,
            jobEtyp,
            GeoParser.get_geo_distance(empCoord, jobCord),
        ]



class RecommendationEngine:


    @staticmethod
    def get_predictions(X):
        if not X:
            return {'predictions':[]}

        response = requests.post(
            url = MODEL_URL,
            json = {
                "data": X
            }
        )
        return response.json()["predictions"]


    @staticmethod
    def get_recommendations(employee, keywords :str=None, n: int = 1000):

        flatten_to_set = lambda x : set(deepflatten(x, depth=1))
        flatten_to_list = lambda x : list(deepflatten(x, depth=1))
        c_split = lambda x : x.split() if type(x) is str else []

        def job_dict(j, fit_ratio, empCord, rat_val):
            return {
                "id":j.id,
                "pos":j.position,
                "comp":j.company,
                "city":j.city,
                "jlat":j.latitude,
                "jlon":j.longitude,
                "elat":empCord[0],
                "elon":empCord[1],
                "decs":j.description,
                "emp_t":empt_d[j.education_required],
                "edu_r":edu_d[j.employment_type],
                "f_factor":fit_ratio,
                "distance":GeoParser.get_geo_distance(
                    empCord,
                    (j.latitude, j.longitude)
                ),
                "rat_val":rat_val
            }

        emprat = { r.job_id: r.rating for r in employee.rating}
        empCord = employee.latitude, employee.longitude
        empAge = (datetime.date.today() - employee.birth_date).days/365
        empInt = flatten_to_set(c_split(x.inter_raw) for x in employee.interest)
        empExperience = employee.experience
        empEDesc = flatten_to_list(c_split(x.desc_raw) for x in empExperience)
        empEPos = flatten_to_set(c_split(x.pos_raw) for x in empExperience)

        keywords_set = set(TxtParser.raw_txt(keywords).split())

        X = []
        sel_j = []

        jobs_k = jobs
        if keywords_set:
            jobs_tmp = set()
            for j in jobs:
                desc_rs = set(c_split(j.desc_raw))
                if len(desc_rs.intersection(keywords_set)) > 0:
                    jobs_tmp.add(
                        j
                    )
            jobs_k = jobs_tmp

        # setup initial filter 
        advert_filter = empEPos.union(keywords_set)
        with_attrs = len(advert_filter) > 0
        if not with_attrs:
            advert_filter = empInt
        with_attrs = len(advert_filter) > 0
        if not with_attrs:
            advert_filter = empEDesc
        with_attrs = len(advert_filter) > 0

        rnd_sset = set()
        if len(jobs_k) < SEARCH_LIMIT:
            rnd_sset = jobs_k
        else:
            rnd_sset =  random.sample(jobs_k, SEARCH_LIMIT)

        for j in rnd_sset:
            if not with_attrs:
                sel_j.append(
                    j
                )
                X.append(
                    DataTools.nn_data_builder(
                        j,
                        empInt,
                        empEPos,
                        empEDesc,
                        empAge,
                        empCord,
                        keywords_set
                    )
                )
            else:
                pos_rs = set(c_split(j.pos_raw))
                if len(pos_rs.intersection(advert_filter)) > 0:
                    sel_j.append(
                        j
                    )
                    X.append(
                        DataTools.nn_data_builder(
                            j,
                            empInt,
                            empEPos,
                            empEDesc,
                            empAge,
                            empCord,
                            keywords_set
                        )
                    )

        X = DataTools.normalize(X)
        p_rat = RecommendationEngine.get_predictions(X)

        sel = []
        for job, ratio in zip(sel_j, p_rat):
            if ratio[0] > 0.5:
                sel.append (
                    job_dict(job, ratio[0], empCord, emprat[job.id] if job.id in emprat else -1)
                )

        sel.sort(
            key= lambda x: x["f_factor"],
            reverse=True
        )

        return sel[:n]
