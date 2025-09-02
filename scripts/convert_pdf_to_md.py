from markitdown import MarkItDown

md = MarkItDown(enable_plugins=False)

docs = [
    "SINEWS_VOLUME4_ISSUE3",
    "SiNEWS (Apr - Jun '25)",
    "SiNEWS_Volume_4_Issue_4",
    "SiNEWS July 2024 (V4_Issue1)",
]

for doc in docs:
    document = md.convert(f"../docs/{doc}.pdf")

    with open("../docs/{doc}.md") as f:
        f.write(document.text_content)
