import unittest
import research_entities as e

class SocialRoles(unittest.TestCase):
 def test_owner_social_not_competitor(self):
  x=e.classify("https://www.facebook.com/andazgoa/posts/example","Moksha Sauna Sessions")
  self.assertEqual(x["role"],"third_party_own_brand_listing")
  self.assertFalse(x["competitor"])
 def test_social_unknown_not_provider(self):
  x=e.classify("https://www.instagram.com/goa_banya/","Russian banya")
  self.assertEqual(x["role"],"third_party_social_listing")
  self.assertFalse(x["competitor"])
 def test_official_provider_site_preserved(self):
  x=e.classify("https://thehiddenoak.space/pricing/","Hidden Oak Pricing")
  self.assertEqual(x["role"],"provider_candidate_needs_review")
if __name__=="__main__":unittest.main()
