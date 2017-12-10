
class Attachment:
    def __init__(self, fallback, **kwargs):
        self.attach = {"fallback": fallback, "fields": []}
        self.attach.update(kwargs)

    def add_field(self, name, value, short=True):
        field = {"title": name, "value": value, "short": short}
        self.attach["fields"].append(field)

    @property
    def data(self):
        return self.attach

    # Attachment Properties
    @property
    def fallback(self):
        return self.attach.get("fallback")

    @property
    def color(self):
        return self.attach.get("color")

    @property
    def pretext(self):
        return self.attach.get("pretext")

    @property
    def author_name(self):
        return self.attach.get("author_name")

    @property
    def author_icon(self):
        return self.attach.get("author_icon")

    @property
    def author_link(self):
        return self.attach.get("author_link")

    @property
    def title(self):
        return self.attach.get("title")

    @property
    def title_link(self):
        return self.attach.get("title_link")

    @property
    def text(self):
        return self.attach.get("text")

    @property
    def image_url(self):
        return self.attach.get("image_url")

    @property
    def thumb_url(self):
        return self.attach.get("thumb_url")

    @property
    def footer(self):
        return self.attach.get("footer")

    @property
    def footer_icon(self):
        return self.attach.get("footer_icon")

    @property
    def ts(self):
        return self.attach.get("ts")

    # Attachment Setters
    @fallback.setter
    def fallback(self, new):
        self.attach.update({"fallback": new})

    @color.setter
    def color(self, new):
        self.attach.update({"color": new})

    @pretext.setter
    def pretext(self, new):
        self.attach.update({"pretext": new})

    @author_name.setter
    def author_name(self, new):
        self.attach.update({"author_name": new})

    @author_icon.setter
    def author_icon(self, new):
        self.attach.update({"author_icon": new})

    @author_link.setter
    def author_link(self, new):
        self.attach.update({"author_link": new})

    @title.setter
    def title(self, new):
        self.attach.update({"title": new})

    @title_link.setter
    def title_link(self, new):
        self.attach.update({"title_link": new})

    @text.setter
    def text(self, new):
        self.attach.update({"text": new})

    @image_url.setter
    def image_url(self, new):
        self.attach.update({"image_url": new})

    @thumb_url.setter
    def thumb_url(self, new):
        self.attach.update({"thumb_url": new})

    @footer.setter
    def footer(self, new):
        self.attach.update({"footer": new})

    @footer_icon.setter
    def footer_icon(self, new):
        self.attach.update({"footer_icon": new})

    @ts.setter
    def ts(self, new):
        self.attach.update({"ts": new})
