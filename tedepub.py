
from bs4 import BeautifulSoup
#from urllib.request import (urlopen, HTTPError)
from urllib import urlopen
from ebooklib import epub
import PIL
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def parse(url):
    bsobj = BeautifulSoup(urlopen(url), "html.parser")
    titleobj = bsobj.find("h4", {"class":"m5"}).a
    authorobj = bsobj.find("h4", {"class":"talk-link__speaker"})
    imgobj = bsobj.find("img", {"class":" thumb__image"})
    paraobj = bsobj.findAll("p", {"class":"talk-transcript__para"})

    #
    title = titleobj.get_text()
    lang = titleobj['lang']
    author = authorobj.get_text()
    imgurl = imgobj['src'].split('?')[0]
    subtitle = ""
    for para in paraobj:
        subtitle = subtitle + "<p>\n"
        subtitle = subtitle + para.data.get_text().strip() + '<br>\n'
        for line in para.span.get_text().split('\n'):
            subtitle = subtitle + line + " "
        subtitle = subtitle + "<br>\n"
        subtitle = subtitle + "</p>\n"

    return (title, lang, author, imgurl, subtitle)

def cover(id, imgurl, title, author):
    cover_path = './cover/' + id + '.jpg'
    coverimg = urlopen(imgurl)
    with open(cover_path, 'wb') as output:
        output.write(coverimg.read())

    im = Image.open(cover_path)
    (width, height) = im.size
    out = im.resize((width, height*3), PIL.Image.ANTIALIAS)

    rectimg = Image.new('RGBA', (width, height*3))
    rectdraw = ImageDraw.Draw(rectimg)
    rectdraw.polygon([(0,height*2), (width, height*2), (width, height*3), (0, height*3)], fill = (10, 15, 70, 60))
    out = Image.alpha_composite(out.convert('RGBA'), rectimg)

    draw = ImageDraw.Draw(out)
    font = ImageFont.truetype("./fonts/NanumMyeongjo.ttf", 180)

    #title.replace(' ', '\n')
    #title = title + '\n - ' + author
    text = ''
    for ln in title.split():
        text = text + ' ' + ln + '\n'
    text = text + ' - ' + author
    draw.multiline_text((0,height*2), text, (255,255,255), font, spacing=15)
    #draw.text((0,height*2), title, (255,255,255), font)

    out.save(cover_path, "JPEG")
    return cover_path
    
def make_epub(id, title, lang, author, cover_path, subtitle):
    book = epub.EpubBook()

    # add metadata
    book.set_identifier('ted_' + id)
    book.set_title(title)
    book.set_language(lang)
    book.add_author(author)

    # add cover image
    book.set_cover("cover.jpg", open(cover_path, 'rb').read())

    chpt = epub.EpubHtml(title='subtitle', file_name='subtitle.xhtml', lang=lang)
    chpt.content='<html><head></head><body>' + subtitle + '</body></html>'
    book.add_item(chpt)

    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    style = 'BODY {color: while;}'
    nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)
    book.add_item(nav_css)
    book.spine = ['nav', chpt]

    epub_path = './epub/' + id + '.epub' 
    epub.write_epub(epub_path, book, {})

    return 

def convert(url):
    id = url.split('/')[4]
    (title, lang, author, imgurl, subtitle) = parse(url)

    cover_path = cover(id, imgurl, title, author)

    make_epub(id, title, lang, author, cover_path, subtitle) 
    return

def main():
    url = "http://www.ted.com/talks/ken_robinson_says_schools_kill_creativity/transcript?language=en"

    convert(url)
    return;

if __name__ == '__main__':
    main()

