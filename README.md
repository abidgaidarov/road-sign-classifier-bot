## Telegram bot for detecting and classifying road signs on a photo

Please open the bot via [link](https://t.me/road_sign_classifier_bot) and press /start.

It is trained on the following classes:
| #      | category                         | description                                                        |
| ------ | -------------------------------- | ------------------------------------------------------------------ |
| 1      | Dangerous warning                | Right bend                                                         |
| 2      | Dangerous warning                | Left bend                                                          |
| 3      | Dangerous warning                | Double bend (left)                                                 |
| 4      | Dangerous warning                | Double bend (right)                                                |
| 5      | Dangerous warning                | Dangerous descent                                                  |
| 6      | Dangerous warning                | Steep ascent                                                       |
| 7      | Dangerous warning                | Carriageway narrows (both)                                         |
| 8      | Dangerous warning                | Carriageway narrows (right)                                        |
| 9      | Dangerous warning                | Carriageway narrows (left)                                         |
| 10     | Dangerous warning                | Road leads on to quay or river bank                                |
| 11     | Dangerous warning                | Uneven road (1 bump)                                               |
| 12     | Dangerous warning                | Uneven road (2 bump)                                               |
| 13     | Dangerous warning                | Slippery road                                                      |
| 14     | Dangerous warning                | Loose gravel                                                       |
| 15     | Dangerous warning                | Falling rocks                                                      |
| 16     | Dangerous warning                | Pedestrian crossing                                                |
| 17     | Dangerous warning                | Children (School)                                                  |
| 18     | Dangerous warning                | Cyclists entering or crossing                                      |
| 19     | Dangerous warning                | Domestic animals crossing                                          |
| 20     | Dangerous warning                | Wild animals crossing                                              |
| 21     | Dangerous warning                | Road works                                                         |
| 22     | Dangerous warning                | Light signals                                                      |
| 23     | Dangerous warning                | Intersection                                                       |
| 24     | Dangerous warning                | Intersection with road                                             |
| 25     | Dangerous warning                | Roundabout                                                         |
| 26     | Dangerous warning                | Level-crossings with gates                                         |
| 27     | Dangerous warning                | Other level-crossings                                              |
| 28     | Dangerous warning                | Level-crossings additional signs                                   |
| 29     | Dangerous warning                | Other dangers                                                      |
| 30     | Dangerous warning                | Snow                                                               |
| 31     | Regulatory - Priority            | Give way                                                           |
| 32     | Regulatory - Priority            | Stop                                                               |
| 33     | Regulatory - Priority            | Priority road                                                      |
| 34     | Regulatory - Priority            | End of priority                                                    |
| 35     | Regulatory - Priority            | Priority for oncoming traffic                                      |
| 36     | Regulatory - Priority            | Priority over oncoming traffic                                     |
| 37     | Regulatory - Prohibitory         | No entry                                                           |
| 38     | Regulatory - Prohibitory         | Closed to all vehicles in both directions                          |
| 39     | Regulatory - Prohibitory         | No entry for cycles                                                |
| 40     | Regulatory - Prohibitory         | No entry for vehicles having an overall height exceeding … meters  |
| 41     | Regulatory - Prohibitory         | No entry for vehicles exceeding … tonnes laden mass                |
| 42     | Regulatory - Prohibitory         | No entry for vehicles having a mass exceeding … tonnes on one axle |
| 43     | Regulatory - Prohibitory         | No entry for trucks                                                |
| 44     | Regulatory - Prohibitory         | No left turn                                                       |
| 45     | Regulatory - Prohibitory         | No right turn                                                      |
| 46     | Regulatory - Prohibitory         | No U-turn                                                          |
| 47     | Regulatory - Prohibitory         | Overtaking prohibited                                              |
| 48     | Regulatory - Prohibitory         | Overtaking by goods vehicles prohibited                            |
| 49     | Regulatory - Prohibitory         | Maximum speed limit 20                                             |
| 50     | Regulatory - Prohibitory         | Maximum speed limit 25                                             |
| 51     | Regulatory - Prohibitory         | Maximum speed limit 30                                             |
| 52     | Regulatory - Prohibitory         | Maximum speed limit 40                                             |
| 53     | Regulatory - Prohibitory         | Maximum speed limit 50                                             |
| 54     | Regulatory - Prohibitory         | Maximum speed limit 60                                             |
| 55     | Regulatory - Prohibitory         | Maximum speed limit 70                                             |
| 56     | Regulatory - Prohibitory         | Maximum speed limit 80                                             |
| 57     | Regulatory - Prohibitory         | Maximum speed limit 90                                             |
| 58     | Regulatory - Prohibitory         | Maximum speed limit 100                                            |
| 59     | Regulatory - Prohibitory         | Maximum speed limit 110                                            |
| 60     | Regulatory - Prohibitory         | Maximum speed limit 120                                            |
| 61     | Regulatory - Prohibitory         | Passing without stopping prohibited                                |
| 62     | Regulatory - Prohibitory         | End of all local prohibitions imposed on moving vehicles           |
| 63     | Regulatory - Prohibitory         | End of maximum speed limit                                         |
| 64     | Regulatory - Prohibitory         | End of prohibition of overtaking                                   |
| 65     | Regulatory - Prohibitory         | End of prohibition of overtaking for goods vehicles                |
| 66     | Regulatory - Prohibitory         | Parking prohibited                                                 |
| 67     | Regulatory - Prohibitory         | Parking prohibited (first half month)                              |
| 68     | Regulatory - Prohibitory         | Parking prohibited (last half month)                               |
| 69     | Regulatory - Prohibitory         | Standing and parking prohibited                                    |
| 70     | Regulatory - Mandatory           | Direction – Straight                                               |
| 71     | Regulatory - Mandatory           | Direction – Right                                                  |
| 72     | Regulatory - Mandatory           | Direction – Left                                                   |
| 73     | Regulatory - Mandatory           | Direction – Straight or Right                                      |
| 74     | Regulatory - Mandatory           | Direction – Straight or Left                                       |
| 75     | Regulatory - Mandatory           | Direction – Turn right                                             |
| 76     | Regulatory - Mandatory           | Direction – Turn left                                              |
| 77     | Regulatory - Mandatory           | Pass Right                                                         |
| 78     | Regulatory - Mandatory           | Pass Left                                                          |
| 79     | Regulatory - Mandatory           | Pass Either side                                                   |
| 80     | Regulatory - Mandatory           | Compulsory roundabout                                              |
| 81     | Regulatory - Mandatory           | Compulsory cycle track                                             |
| 82     | Regulatory - Mandatory           | Compulsory cycle track - footpath                                  |
| 83     | Regulatory - Mandatory           | Compulsory cycle track - footpath                                  |
| 84     | Regulatory - Mandatory           | Compulsory bus                                                     |
| 85     | Regulatory - Mandatory           | End of compulsory cycle track                                      |
| 86     | Regulatory - Special regulations | One-way (Straight)                                                 |
| 87     | Regulatory - Special regulations | One-way (Right)                                                    |
| 88     | Regulatory - Special regulations | Motorway                                                           |
| 89     | Regulatory - Special regulations | Beginning of area                                                  |
| 90     | Regulatory - Special regulations | End of area                                                        |
| 91     | Regulatory - Special regulations | Maximum speed zone                                                 |
| 92     | Regulatory - Special regulations | End of maximum speed zone                                          |
| 93     | Regulatory - Special regulations | Pedestrian crossing                                                |
| 94     | Regulatory - Special regulations | Parking                                                            |
| 95     | Regulatory - Special regulations | Parking for handicap                                               |
| 96     | Regulatory - Special regulations | Parking for cars                                                   |
| 97     | Regulatory - Special regulations | Parking for bus                                                    |
| 98     | Regulatory - Special regulations | Parking on pavement or verge                                       |
| 99     | Regulatory - Special regulations | Parking on the right                                               |
| 100    | Others                           | Curve left                                                         |
| 101    | Others                           | Barrier                                                            |
| 102    | Others                           | Obstacle                                                           |

