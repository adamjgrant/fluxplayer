class Image():
  def __init__(self, url, description):
    self.url = f"https://cdn.everything.io/chatgpt/maura/{url}"
    self.description = description

  def markdown(self):
    return f"![{self.description}]({self.url})\n_{self.description}, [Open image in new window]({self.url})_\n\n"
