from django.test import TestCase
from django.urls import reverse

from mainapp.models import Location, Model
from mainapp.tests.mixins import BaseViewTestMixin


class SearchViewTest(BaseViewTestMixin, TestCase):
    """Tests for the search view in the mainapp."""

    def test_search_view_no_params_renders_empty_filter_form(self):
        response = self.client.get(reverse("search"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["searched"])
        self.assertIsNone(response.context["models"])
        self.assertContains(response, 'id="search-filters"')
        self.assertNotContains(response, "No models were found with those parameters.")
        self.assertNotContains(response, "Model 1")

    def test_search_by_title(self):
        response = self.client.get(reverse("search"), {"query": "Model 1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 1")
        self.assertNotContains(response, "Model 2")
        self.assertNotContains(response, "Model 3")
        self.assertEqual(len(response.context["models"]), 1)

    def test_search_by_tag_filter(self):
        response = self.client.get(reverse("search"), {"tag": "color=red"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 1")
        self.assertNotContains(response, "Model 2")
        self.assertNotContains(response, "Model 3")

    def test_invalid_tag_shows_error(self):
        for bad in ("invalidtag", "=yes"):
            response = self.client.get(reverse("search"), {"tag": bad})
            self.assertEqual(response.status_code, 200)
            self.assertFalse(response.context["searched"])
            self.assertIsNone(response.context["models"])
            self.assertContains(response, "Invalid tag")
            self.assertNotContains(response, "Model 1")

    def test_tag_value_may_contain_equals(self):
        self.model1.tags = {"note": "a=b"}
        self.model1.save()
        response = self.client.get(reverse("search"), {"tag": "note=a=b"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 1")

    def test_search_by_category(self):
        response = self.client.get(reverse("search"), {"category": "category1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Model 1")
        self.assertNotContains(response, "Model 2")

    def test_query_and_category_combine(self):
        # Model 3 shares no category with Model 1; a category filter alone
        # would return Model 1, but the text query must also match.
        response = self.client.get(
            reverse("search"), {"query": "Model 1", "category": "category1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["models"]), 1)
        self.assertContains(response, "Model 1")

        response = self.client.get(
            reverse("search"), {"query": "Model 3", "category": "category1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["models"])
        self.assertContains(response, "No models were found with those parameters.")

    def test_query_and_tag_combine(self):
        response = self.client.get(
            reverse("search"), {"query": "Model 3", "tag": "color=red"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["models"])

        response = self.client.get(
            reverse("search"), {"query": "Model", "tag": "color=red"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["models"]), 1)
        self.assertContains(response, "Model 1")

    def test_category_and_tag_combine(self):
        response = self.client.get(
            reverse("search"), {"category": "category1", "tag": "size=large"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["models"]), 1)
        self.assertContains(response, "Model 1")

        response = self.client.get(
            reverse("search"), {"category": "category1", "tag": "size=small"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["models"])

    def test_category_dropdown_lists_visible_categories(self):
        response = self.client.get(reverse("search"), {"category": "category1"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("category1", response.context["categories"])
        # category2 only belongs to a hidden model, so a normal user must not see it.
        self.assertNotIn("category2", response.context["categories"])
        self.assertContains(response, '<option value="category1" selected>')

        self.login_user("admin")
        response = self.client.get(reverse("search"))
        self.assertIn("category2", response.context["categories"])

    def test_active_filter_removal_links(self):
        response = self.client.get(
            reverse("search"), {"query": "Model", "category": "category1", "tag": "color=red"}
        )
        self.assertEqual(response.status_code, 200)
        links = response.context["remove_links"]
        self.assertNotIn("query=", links["query"])
        self.assertIn("category=category1", links["query"])
        self.assertIn("tag=color%3Dred", links["query"])
        self.assertNotIn("category=", links["category"])
        self.assertNotIn("tag=", links["tag"])

    def test_hidden_model_not_shown_to_user(self):
        response = self.client.get(reverse("search"), {"query": "Model 2"})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["models"])

    def test_hidden_model_shown_to_admin(self):
        self.login_user("admin")
        response = self.client.get(reverse("search"), {"query": "Model 2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["models"]), 1)
        self.assertEqual(response.context["models"][0].model_id, 2)

    def test_search_pagination(self):
        for i in range(10):
            m = Model.objects.create(
                model_id=100 + i,
                revision=1,
                title=f"Paginated {i}",
                author=self.user,
                is_hidden=False,
                location=Location.objects.create(latitude=0, longitude=0),
                tags={},
                license=0,
                latest=True,
            )

        page1 = self.client.get(reverse("search"), {"query": "Paginated", "page": 1})
        page2 = self.client.get(reverse("search"), {"query": "Paginated", "page": 2})

        self.assertEqual(page1.status_code, 200)
        self.assertEqual(page2.status_code, 200)
        self.assertEqual(len(page1.context["models"]), 6)
        self.assertEqual(len(page2.context["models"]), 4)

    def test_search_no_results(self):
        response = self.client.get(reverse("search"), {"query": "nohits"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No models were found with those parameters.")
        self.assertIsNone(response.context["models"])

    def test_url_params_context(self):
        response = self.client.get(
            reverse("search"), {"query": "Model", "category": "category1"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("query=Model", response.context["url_params"])
        self.assertIn("category=category1", response.context["url_params"])

    def test_url_params_are_encoded_and_separated(self):
        response = self.client.get(
            reverse("search"), {"query": "Model 1 & co", "tag": "color=red"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["url_params"], "?query=Model+1+%26+co&tag=color%3Dred"
        )
        # Pagination links must round-trip through the same view.
        for i in range(10):
            Model.objects.create(
                model_id=100 + i,
                revision=1,
                title=f"Model 1 & co {i}",
                author=self.user,
                is_hidden=False,
                location=Location.objects.create(latitude=0, longitude=0),
                tags={"color": "red"},
                license=0,
                latest=True,
            )
        response = self.client.get(reverse("search"), {"query": "Model 1 & co"})
        self.assertContains(response, 'href="/search?query=Model+1+%26+co&page=2"')
        response = self.client.get("/search?query=Model+1+%26+co&page=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["models"]), 4)

    def test_last_page_updated(self):
        self.client.get(reverse("search"), {"query": "Model"})
        self.assertTrue(
            self.client.session.get("last_page").startswith(reverse("search"))
        )
