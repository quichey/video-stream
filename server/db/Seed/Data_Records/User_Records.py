"""
Data_Records
uses VideoFileManager in db/Schema/Video
to create Video Record

For profile picture, want to do something similar
but images can be placed in multiple tables i think
as user can have multiple picturs for their channel/homepage

so thinking maybe db/Schema/Img

or generalize the VideoFileManager to be some abstract FileManager
for assets difficult to store in RDBMS systems

TBH, don't necessarily need to randomize the generation 
of profile pics. Can just data-entry it into the db for testing

DO need some sort of enforced pathways to the stored images 
and eventually same way for user to upload images
"""
## 