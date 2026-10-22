#!/usr/bin/env python3
import datetime as dt
import tempfile
import unittest
import gsc_multidim as m
SITE="https://mokshagoa.com/"
def report():
    return {"site":SITE,"source":"engagement_core_read_only",
            "dimensions":["query","page","country","device","date"],
            "start_date":"2026-10-10","end_date":"2026-10-17",
            "row_limit":25000,"start_row":0,
            "rows":[{"keys":["sauna arambol","https://mokshagoa.com/","ind","MOBILE","2026-10-16"],
                     "clicks":3,"impressions":52,"ctr":3/52,"position":7.2},
                    {"keys":["sauna arambol","https://mokshagoa.com/","ind","MOBILE","2026-10-17"],
                     "clicks":4,"impressions":61,"ctr":4/61,"position":6.5}]}
class GSCTests(unittest.TestCase):
    def test_scope_valid(self):
        self.assertEqual(m.validate(report(),SITE)["rows"],2)
    def test_wrong_site_rejected(self):
        with self.assertRaises(ValueError):m.validate(report(),"https://other.example/")
    def test_wrong_dimensions_rejected(self):
        r=report();r["dimensions"]=["query"]
        with self.assertRaises(ValueError):m.validate(r,SITE)
    def test_bad_source_rejected(self):
        r=report();r["source"]="unknown_csv"
        with self.assertRaises(ValueError):m.validate(r,SITE)
    def test_bad_date_rejected(self):
        r=report();r["rows"][0]["keys"][4]="2020-01-01"
        with self.assertRaises(ValueError):m.validate(r,SITE)
    def test_paging_limit_rejected(self):
        r=report();r["row_limit"]=25001
        with self.assertRaises(ValueError):m.validate(r,SITE)
    def test_metric_validation(self):
        r=report();r["rows"][0]["clicks"]=1000
        with self.assertRaises(ValueError):m.validate(r,SITE)
    def test_bad_device(self):
        r=report();r["rows"][0]["keys"][3]="SMART_TV"
        with self.assertRaises(ValueError):m.validate(r,SITE)
    def test_row_insert_and_duplicate(self):
        with tempfile.TemporaryDirectory() as p:
            db=m.db_open(p+"/gsc.sqlite")
            self.assertEqual(m.import_report(db,report(),SITE)["inserted"],2)
            self.assertEqual(m.import_report(db,report(),SITE)["status"],"duplicate")
            self.assertEqual(db.execute("SELECT count(*) FROM gsc_observation").fetchone()[0],2)
            db.close()
    def test_click_and_impression_delta(self):
        with tempfile.TemporaryDirectory() as p:
            db=m.db_open(p+"/gsc.sqlite");m.import_report(db,report(),SITE)
            out=m.compare(db,SITE,"2026-10-16","2026-10-17")
            self.assertEqual(out["deltas"][0]["click_delta"],1)
            self.assertEqual(out["deltas"][0]["impression_delta"],9)
            self.assertTrue(out["site_only"])
            db.close()
    def test_bound_compare(self):
        with tempfile.TemporaryDirectory() as p:
            db=m.db_open(p+"/gsc.sqlite")
            with self.assertRaises(ValueError):m.compare(db,SITE,"2026-10-16","2026-10-17",limit=25)
            db.close()
if __name__=="__main__":unittest.main(verbosity=2)
