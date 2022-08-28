# How to generate the link
# 1 - from https://edt.grenoble-inp.fr 
# 2 - Navigate to your edt with the small arrows
# 3 - then click on "export agenda" and then "generer url"
# 4 - copy the url
# 5 - Insert your uid and passwd from your personal account after https:// with the following syntax
# example:
# genrated url: https://edt.grenoble-inp.fr/directCal/2022-2023/etudiant/phelma?resources=20868,5574
# autheticated url: https://uid:passwd@edt.grenoble-inp.fr/directCal/2022-2023/etudiant/phelma?resources=20868,5574
#
ICAL_FEED = 'https://uid:passwd@edt.grenoble-inp.fr/directCal/2022-2023/etudiant/phelma?resources=20868,5574'

# To filter out useless events, you have to provide a string that matches the name of the event 
# and a string that match the description to keep
# all events matching the name and not the description are removed from the event list
# The following example remove all English event but group 4, all Math&Physic but group 7 and all Sports 
# as the second string never matches any event description
#
SET_TO_REMOVE=(("impossible to find","impossible to find"),("impossible to find","impossible to find"))
