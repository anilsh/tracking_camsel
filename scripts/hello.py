
(img_8842:Photo) -[:DEPICTS]-> (p1:Person {name: '<you>'})
​(img_8842:Photo) -[:DEPICTS]-> (p2:Person {name: 'Amy'})
​(img_8842:Photo) -[:CONTAINS]-> (c1:Concept {name: 'outfit'})
​(img_8842:Photo) -[:CONTAINS]-> (c2:Concept {name: 'tuxedo'})
​(img_8842:Photo) -[:PART_OF]-> (e1:Event {name: "Amy's Wedding"})
​(e1:Event) -[:OCCURRED_AT]-> (l1:Location {name: 'St. Peter's Church'})
​(p1:Person) -[:ATTENDED]-> (e1:Event)

{
  "photo_id": "img_8842.jpg",
  "main_event": {
    "name": "Amy's Wedding",
    "location": "St. Peter's Church"
  },
  "people_detected": [
    {
      "name": "<you>",
      "relation_to_event": "ATTENDED"
    },
    {
      "name": "Amy",
      "relation_to_event": "ATTENDED"
    }
  ],
  "concepts_of_interest": [
    "outfit",
    "tuxedo"
  ]
}
