import gdata.photos.service
import gdata.media
import gdata.geo

email = 'prodmand@gmail.com'
password = 'asdF!234'
username = 'prodmand'

gd_client = gdata.photos.service.PhotosService()
gd_client.email = email
gd_client.password = password
gd_client.source = 'exampleCo-exampleApp-1'
gd_client.ProgrammaticLogin()

albums = gd_client.GetUserFeed(user=username)
for album in albums.entry:
    print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
                                                       album.numphotos.text, album.gphoto_id.text)
    print album.GetHtmlLink().href

photos = gd_client.GetFeed(
    '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
        username, '5452249956568940705'))
for photo in photos.entry:
    print photo.title.text, photo.GetHtmlLink().href