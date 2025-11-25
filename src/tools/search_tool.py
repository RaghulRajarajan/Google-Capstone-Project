import json

class SearchTool:
    def __init__(self, file_path="labeled_test.json"):
        with open(file_path, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def search(self, query):
        results = []
        q = query.lower()

        for item in self.data:
            text = item.get("text", "").lower()
            if q in text:
                results.append(item)

        return results


if __name__ == "__main__":
    st = SearchTool()
    keyword = input("Enter search keyword: ")
    matches = st.search(keyword)
    print(json.dumps(matches, indent=2))
