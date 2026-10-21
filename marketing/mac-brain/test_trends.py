#!/usr/bin/env python3
"""Offline verification for public Google Trends signals and normalization."""
from datetime import datetime,timezone
from email.utils import format_datetime
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

FILE=Path(__file__).with_name("trends.py")
class TrendsTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        spec=importlib.util.spec_from_file_location("trends_unit",FILE)
        self.mod=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.mod.DATABASE=Path(self.temp.name)/"trends.sqlite3"
        self.mod.INBOX=Path(self.temp.name)/"trends-inbox"
        self.mod.INBOX.mkdir()
    def tearDown(self): self.temp.cleanup()
    def sample(self):
        stamp=format_datetime(datetime.now(timezone.utc))
        xml=f"""<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0" xmlns:ht="https://trends.google.com/trending/rss">
        <channel><item><title>sauna and cold plunge India</title>
        <pubDate>{stamp}</pubDate><ht:approx_traffic>1K+</ht:approx_traffic>
        <ht:news_item><ht:news_item_title>Sauna travel news</ht:news_item_title></ht:news_item>
        </item></channel></rss>"""
        return xml.encode()
    def test_parser_keeps_traffic_band_separate(self):
        data=self.mod.parse_rss(self.sample(),"IN")
        self.assertEqual(len(data),1)
        self.assertEqual(data[0]["approx_traffic"],"1K+")
        self.assertEqual(data[0]["term"],"sauna and cold plunge India")
    def test_ingest_matches_and_never_guesses_volume(self):
        def f(g):return self.mod.parse_rss(self.sample(),g)
        result=self.mod.refresh("IN",f)
        self.assertEqual(result["status"],"updated")
        insights=self.mod.brief_context("sauna wellness travel", "IN")
        self.assertTrue(insights["rss_signal"])
        self.assertIn("absolute monthly search volume",insights["do_not_infer"])
        self.assertFalse(insights["publish_approval"])
        self.assertEqual(self.mod.refresh("IN",f)["status"],"cached")
    def test_csv_normalized_by_export_group(self):
        (self.mod.INBOX/"export.csv").write_text(
            "Day,sauna: (India),ice bath: (India)\n2026-10-19,85,30\n2026-10-20,100,65\n")
        result=self.mod.import_csv("export.csv","IN","2026_10_week")
        self.assertEqual(result["items"],4)
        data=self.mod.brief_context("sauna","IN")
        self.assertEqual(len(data["historical_comparison_groups"]),1)
        self.assertIn("sauna", data["historical_comparison_groups"][0]["series"])
    def test_private_paths_and_bad_series_rejected(self):
        with self.assertRaises(ValueError):self.mod.import_csv("../data.csv")
        with self.assertRaises(ValueError):self.mod.import_csv("a.csv",window="../bad")
    def test_invalid_geo_rejected(self):
        with self.assertRaises(ValueError):self.mod.refresh("XX",lambda x:[])
    def test_no_data_has_no_fake_trend(self):
        v=self.mod.brief_context("arambol yoga","IN")
        self.assertTrue(v["no_verified_relevance"])
        self.assertFalse(v["rss_signal"])
if __name__=="__main__":unittest.main(verbosity=2)
