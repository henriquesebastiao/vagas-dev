with open('CHANGELOG.md', 'r', encoding='utf-8') as changelog:
    text = changelog.read()
    with open('docs/changelog.md', 'w', encoding='utf-8') as doc_changelog:
        doc_changelog.write("""---
icon: lucide/scroll-text
hide:
    - toc
---\n\n""")
        doc_changelog.write('# Changelog\n\n')
        doc_changelog.write(text)
