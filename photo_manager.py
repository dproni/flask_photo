import gdata.photos.service
import gdata.media
import gdata.geo
import pymongo

class PicasaPhotos(object):

    def __init__(self):
        self.email = 'lenkyc@gmail.com'
        self.password = 'xsW23Edc'
        self.username = 'lenkyc'

    def get_albums(self):
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = self.email
        gd_client.password = self.password
        gd_client.source = 'exampleCo-exampleApp-1'
        gd_client.ProgrammaticLogin()
        albums = gd_client.GetUserFeed(user=self.username)
        album_list = []

        for album in albums.entry:
            data = dict()
            data['title'] = album.title.text
            data['count'] = album.numphotos.text
            data['description'] = album.gphoto_id.text
            data['link'] = album.GetHtmlLink().href
            album_list.append(data)
        return album_list

    def get_photos(self, album):
        gd_client = gdata.photos.service.PhotosService()
        gd_client.email = self.email
        gd_client.password = self.password
        gd_client.source = 'exampleCo-exampleApp-1'
        gd_client.ProgrammaticLogin()
        photos = gd_client.GetFeed('/data/feed/api/user/%s/albumid/%s?kind=photo&thumbsize=160c' % (self.username, album))
        photo_list = []
        for photo in photos.entry:
            data = dict()
            data['title'] = photo.title.text
            data['album'] = album
            data['thumbnail'] = photo.media.thumbnail[0].url
            data['link'] = photo.content.src
            photo_list.append(data)
        return photo_list

conn = pymongo.Connection()

conn = pymongo.Connection('localhost', 27017)

db = conn['photos']

coll = db.mycoll

coll = db['albums']

a = PicasaPhotos()
album_list = a.get_albums()
coll.remove({})
for album in album_list:
    coll.save(album)

album = '5854564930649852097'
coll = db['photos']
coll.remove({})
for photo in a.get_photos(album):
    coll.save(photo)

conn.close()



