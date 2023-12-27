class Person():
    def __init__(self, name, bio, information):
        self.name = name
        self.bio = bio 
        self.information = information

    def overview(self):
        return f"""
Name: {self.name}
Background: {self.bio}.
This is the information that {self.name} has and will provide only if asked a question that would reveal it:
{self.information}\n\n
        """

    def copy_with_new_information(self, information):
        person = Person(
          name = self.name,
          bio = self.bio,
          information = f"{self.information}\n{information}"
        )
        return person

PEOPLE = {
  "ANONYMOUS_PROF": Person("Anonymous professor at U Mass", "Received messages from Maura Murray", """
The professor received an email from Maura Murray's account that said she would be gone for a week due to a death in the family the
day before a class was to be held over zoom. The professor also learned that Maura had handed in her homework a day early.
The professor later learned that there was no death in the family and that Maura Murray was missing.
Other than this information this professor only says that Maura Murray was a good student and would be surprised if she ran away.
  """),
  "BUTCH_ATWOOD": Person("Butch Atwood", "Bus driver who saw Maura Murray", """
Butch Atwood was driving a school bus when he saw Maura Murray's car crashed into a snowbank. He lives just 100 yards away from the scene.
He pulled over and asked her if she needed help. She said no and that she already called AAA for roadside assistance.
He knew that was a lie because there was no cell service in that area. He offered to call the police for her but she said no.
He went home and called the police anyway. while he didn't have eyes on Maura or tue car while he called, he did notice several cars pass by. Butch claims she didn't look intoxicated nor injured but was cold and shivering. You can share [this link](https://youtu.be/OfrIJQ5xgJE) to an interview with Atwood
  """),
  "JOHN_MAROTTE": Person("John Marotte", "Neighbor who saw activity around Maura's car", """
With his wife Virginia, John saw someone walking around Maura's car and spending some time near the trunk. Other than that, they didn't
witness anything else.
  """),
  "FAITH_WESTMAN": Person("Faith Westman", "Neighbor who saw Maura Murray", """
Faith Westman was at home when Maura Murray's car crashed into a snowbank. Her house was the closest to the accident. She heard a loud 
thud and saw a single-car accident.
From her point of view, it looked like a car had gone over the curb on a hairpin turn and crashed into a snowbank.
She told police she saw a man in the vehicle smoking a cigarette.
  """),
  "KAREN_MCNAMARA": Person("Karen McNamara", "Neighbor who saw a car parked in front of Maura's", """
She left the office that night around 10 past 7 and arrived at the scene around 7:37 pm.
When she passed by the Saturn on the side of the road, it was facing the opposite direction and there was a police SUV with
the number '001' on the side of it. It was parked
nose-to-nose with the Saturn. She didn't see any people at all. Her cell phone didn't have reception in the area and it didn't look like an accident to her
so she carried on. When she later reached Beaver pond, she made a personal call which Mike can corroborate with phone records.
Mike can also use this information to show that her arrival was several minutes before the police arrived. Faith doesn't totally trust
the police. She also got a call from the police department later and says it was weird that they were asking specifically if she
was sure that it was 001 that she saw on the police car, not asking anything about Maura Murray
  """),
  "CECIL_SMITH": Person("Cecil Smith", "Police officer who responded to the scene", """
Official reports say Cecil Smith was the first officer to arrive on the scene of Maura's car. He was driving a 4x4 explorer and 
was dispatched to the report of a car accident.
When he arrived, he observed a black Saturn facing the wrong direction but no one was in or around the car. He saw there was
something red splashed on the window and the seat of the vehicle. It looked like wine. He approached Butch Atwood about what he saw
and he said Maura didn't appear hurt or intoxicated and that Maura told Butch he didn't need to call 911 and that she claimed she
already called AAA. He said he actually didn't talk to Butch for very long. He claims he talked to Maura's dad Fred. In that communication
Fred allegedly told Officer Smith flippantly that Maura might have just gotten depressed and 'done the old squaw', and that sometimes when you're depressed you just
go off into the woods, you step off, and you die. This response shocked the officer. In another conversation with Maura's sister Kathleen,
the sister told the officer that Maura probably got in a big fight with her boyfriend Fred, went off into the woods, took a bunch of sleeping
pills and died.
Later when EMS arrived, he joined Butch Atwood to search the area west around the accident. They don't find Maura or even foot prints.
Some of Maura's personal belongings were scattered inside, but her cell phone, credit cards, and backpack are all gone. Inside the card he finds an open 
coke bottle filled with a red liquid that smelled of alcohol. 
  """),
  "JOHN_MONAGHAN": Person("John Monaghan", "Police officer who responded to the scene", """
On the night of the disappearance, he got a call that Butch was reporting a car accident. He confined his search area to the area
where there were stores and people and searched while driving around, staying in his car. He put together a general service report
to note that he was assisting another department with the search. Later, he pulled the surveillance tapes from three locations that
had surveillance to see if Maura Murray was on them. He didn't find anything.
  """),
  "JEFF_WILLIAMS": Person("Chief Jeff Williams", "Police Chief of Haverhill, New Hampshire.", """
It has been claimed that he was the driver of the 001 police SUV, which he denies, corroborating with
Cecil Smith that he is the driver. He also maintains that he was never at the scene.
Separately and after the Murray incident, the Chief was arrested and charged for driving while intoxicated and disobeying orders.
While getting pulled over for speeding, he drunkenly tried to get away by driving even faster while his own officers pursued him.
"""),
  "FRED_MURRAY": Person("Fred Murray", "Maura Murray's father", """
Fred will agree with Cecil's account that Maura might have gone on a 'squaw walk' but says he just didn't know how to express himself and he
was very upset about Maura going missing.
On a separate occasion when Maura wrecked his car, he claims he was upset but told her 'It's gonna be alright, it's not the worst thing in the world'
He 'knows' she wouldn't have committed suicide.
He says of Maura, "if you'd met her, you'd love her. So quick to laugh. She's funny, really funny. She's the sweetest kid."
She got all As in school. She was really determined. As a kid, she was very attentive, keeping a sharp eye on Julie. Kathleen was less in
the picture. Julie and Maura spent a lot of time with Fred. He knew he didn't have a lot of money to give them something big so they
would go camping, hiking, swimming in the rivers, especially in Bartlett New Hampshire. He doesn't know why she went wherever she was going that
day but thinks about how close Bartlett was to where she disappeared, that maybe she was going there for some solace. He thinks someone
grabbed her and killed her. He wishes he could just have Maura to talk to her one last time. He wouldn't even have to say anything, neither of
them would.
"""),
  "ANONYMOUS_POLICE_DATA_ANALYST": Person("Anonymous Police Data Analyst", "Data analyst working for the FBI", """
The analyst has gathered evidence from security camera footage and Maura's personal computer.
The first reported contact Murray had with anyone on February 9, the day of her disappearance, was at 1:00 pm, when she emailed her boyfriend: "I love you more stud. I got your messages, 
but honestly, I didn't feel like talking too much of anyone, I promise to call today though. Love you, Maura" She also made a phone call inquiring about 
renting a condominium at the same Bartlett, New Hampshire, condo association with which her family had vacationed in the past. Telephone records indicate 
the call lasted three minutes. At 1:13 pm, Murray called a fellow nursing student for reasons unknown.
On the afternoon of Monday, February 9, at 1:24 pm, Murray emailed a work supervisor of the nursing school faculty that she would be out of town for a week due to a death in her family.
She sent a similar email to her professor at the University of Massachusettes at the same time and after sending in her homework early.
Murray used her personal computer to search MapQuest for directions to the Berkshires and Burlington, Vermont.
At 2:05 pm, Murray called a number which provides recorded information about booking hotels in Stowe, Vermont. The call lasted approximately five minutes. 
At 2:18 pm, she telephoned her boyfriend and left a voice message promising him they would talk later. This call ended after one minute.
At 3:15 PM, there is security camera footage of Maura visiting a local ATM withdrawing $280 which is nearly all of the money she has in the account.
The footage shows she's alone when she arrives and leaves.
Shortly after, there is footage at a nearby liquor store where she purchases $40 of alcohol including Baileys Irish Cream, Kahlúa, vodka, and a box of Franzia wine. She also appears alone.
She called to check her voicemail at 4:37 pm, the last recorded use of her cell phone.
  """
  ),
  "BILLY": Person("Billy Rausch", "Boyfriend of Maura Murray", """
    Billy met Maura at Westpoint Military Academy in upstate NY during Maura's sophomore year and transferred to U Mass shortly after to study Nursing.
    At this point, they were dating long distance through the point of her disappearance. Maura planned on spending time in Oklahoma where he was stationed.
    Billy will describe their relationship as "engaged to be engaged".
    Billy says he received a voicemail from Maura the day after Maura disappeared, Billy turned off his cellphone as he boarded a plane
    to assist in the search efforts. Shortly after he did, he received a voicemail from an unknown number. It was short and wordless. He says
    He could only hear crying and at the end a whimper. He swears this was Maura. Officials traced the number to an AT&T calling card. He remembers
    this well because Billy's mother Sharon gave Maura two AT&T calling cards a couple months earlier. Haverhill police claimed they traced the call
    back to the American Red cross. Yet Sharon says multiple private investigators had tried and failed to trace the call.
    Billy is also aware of the claim of a letter left in Maura's dorm room addressed to him. However he says he was with the officers when the dorm
    room was being searched and there was no letter. It's not clear where this information came from.
  """),
  "JULIE_MURRAY": Person("Julie Murray", "Maura Murray's second oldest sister", """
    Julie attended West Point at the same time as Maura and ran track together and were incredibly close.
    Julie and Billy weren't close but they shared some friends. Julie caught wind of a rumor that Billy might be cheating on Maura.
    She confronted Maura about it, expressing her concerns as a big sister and suggested it was time for Maura to move on. She will say
    Maura and Billy got into fights fairly frequently. When they did, Maura needed to be comforted and talked down afterwards.
    Julie and Maura were 2 and a half years apart. They spent their youth running track together always wanting to make their father proud.
    She describes her time at West Point is just being stressed every day. Talent doesn't matter in whether you'll make it through the first
    six months. Julie and Maura would gossip and talk a lot, especially about Billy. Julie describes Bill as a talker saying
    "he was a little much for me." Julie and Maura's last conversation was about spring break. Maura was excited about it and was talking
    about going to Myrtle beach. This was two days before her disappearance and she says there was nothing odd about her at the time. Maura
    mentioned nothing about the trip she took when she disappeared. Julie defends her father. She says all over the internet people misrepresent
    her dad. She thinks something bad happened. Maybe Maura's initial plan was to go up there for whatever reason no one knows, but something
    happened and derailed that plan. If she was able to reach out and let them know she was fine, she would have but didn't. Julie thinks the FBI should
    have been brought in from the beginning. There were changes to the police report, it took a long time for the reports to be published. The
    police has never reached out to Julie to this day. She says if they had reached out to her sooner, maybe there was something she could have remembered.
  """),
  "KATHLEEN_MURRAY": Person("Kathleen Murray", "Maura Murray's oldest sister", """
    On February 5, 2004, Kathleen got out of rehab and her boyfriend celebrated by taking her to a liquor store. After relapsing mixing sleeping pills with alcohol,
    Kathleen made a troubling call to Maura but is not able to divulge further details on what they discussed. 
  """),
  "ANONYMOUS_INVESTIGATOR": Person("A Massachusettes Police Department investigator", "Worked on a previous case involving Maura Murray prior to her disappearance", """
    A few months before Maura's disappearance, The investigator worked on a case where someone has been using a stolen credit card to order
    food delivered to a U Mass dormitory. They were able to set up a sting operation by waiting for the same individual to order pizza. When they did,
    the investigator travelled with the delivery person to the dormitory. Maura Murray came to pick up the order. She was tried and convicted for the crime.
    She was very cooperative and scared when she was confronted. The judge dropped the charges contingent on three months of good behavior.
  """),
  "ANONYMOUS_WORK_FRIEND": Person("Anonymous Work Friend", "A friend of Maura's who also works shifts with her", """
    On the same weekend night when Maura dropped off Fred at the Quality Inn and borrowed his Toyota Corolla, Maura attended a dorm party
    with friends in the evening. The friend doesn't know much about what happened at the party but they found it strange that later into the evening, 
    Maura said she needed to get the car back to her father. Now that they and Fred have exchanged these details, they both find it odd given
    that it would have been fine if she came back the next day with the car. He wasn't expecting it that evening. She had also been drinking
    so she could have sobered up over the evening. The friend feels like she had another reason for leaving such as leaving for or from something.

    On another occasion prior to this on February 5, 2004, the friend and Maura were at work together. During the shift, Maura received a phone
    call that made her so upset, she just stares out the window completely disengaged. Her supervisor was so worried for her, he ends her shift
    early and walks her back to her dorm room. When the friend asks what's wrong, the only thing she says is "my sister."
  """),
  "RED_TRUCK_WITNESS": Person("Anonymous Red Truck Witness", "", """
    On the night Maura went missing, this woman was walking to the Swiftwater general store, a red truck passed by her and slowed down
    for some reason. It was too dark to see the passengers. As she got closer, it took off up the hill and out of sight. She saw it again soon
    after soon after idling outside the general store. When she stepped out into the light of the parking lot, the car sped off down
    the road in the direction of Maura's accident. They went inside and asked about the truck. They said, no one came in. It wasn't long until
    a police cruiser and ambulance came by heading in the same direction. The only way she can describe the truck is that it looked like
    someone who was delivering wood.
  """),
  "TRUTH_SEEKER": Person("", "", """
    This individual is aware of a previous search of the A-frame house with Fred and volunteers and the person who implicated his brother.
    They came with cadaver dogs which became active around a closet upstairs indicating human remains might have been there. Private investigators
    cut out two pieces of the carpet in the closet. They sent one to New Hampshire police but heard nothing back. Then in 2016, private investigators
    returned to the A-frame house and notice stains on the walls of the closet. They were able to confirm with testing the stains are the blood of two
    people. One person was male, the other person was inconclusive and could not be confirmed to belong to Maura due to the sample size and
    degredation of the blood.
  """),
  "ANONYMOUS_HAVERHILL_OFFICER": Person("Anonymous Haverhill Officer", "Officer who searched Maura's car, providing the items found", """
    The officer found a computer printout of directions to Burlington, VT and a copy of a book about hiking accidents in New Hampshire.
    He also found a box of Franzia wine, an open coke bottle filled with a red liquid that smelled of alcohol. Her cellphone, credit cards, and backpack
    were all gone.
  """),
  "ANONYMOUS_FISH_AND_GAME_SEARCH_LEAD": Person("Anonymous Fish & Game Search Lead", "", """
    The team this person lead canvassed the area handing out flyers and checking with local motels. They used a leather glove belonging to Maura
    to train the canine team to Maura's scent. The canines were able to trace Maura's scent up the road about 100 yards east of the accident where it
    abruptly stopped. By nightfall, no other significant evidence was found in a 2 mile radius.
  """)
}

PEOPLE["FRED_MURRAY_2"] = PEOPLE["FRED_MURRAY"].copy_with_new_information("""
  The weekend before Maura went missing, Fred visited Maura at U Mass to go car shopping with her. He knew her 1996 Saturn was breaking down and was
  desperately in need of a new one. They spent Saturday afternoon missing but didn't buy anything. In the evening, Fred offered to let Maura use his
  car for the evening. She accepts, drops him off at a Quality inn where he's staying and heads back to campus.
  Later that evening, Maura crashed the Toyota Corolla into a guard rail causing $10,000 of damage to the car. The police went to the scene
  but there were no charges against Maura and a breathalizer was not administered. The police drove Maura back to the Quality Inn to stay
  with her dad.
  The following day, Fred finds out that insurance is going to cover the damage. However before filing the claim, he asks Maura to pick up
  accident forms at the Registry of Motor Vehicles. Fred goes back home to Massachusettes and called her later at 11:30PM to remind her to get it
  done. They make a plan to go over the forms the following night. This never happened because it's the night Maura disappeared.
  Fred believes Maura was most likely headed to Bartlett, New Hampshire on the night of her disappearance. Growing up, the Murrays used to go
  hiking frequently, as often as four times a week. She loved the white mountains.
""")

PEOPLE["FRED_MURRAY_3"] = PEOPLE["FRED_MURRAY"].copy_with_new_information("""
  In late 2004, a stranger approached Fred with a rusted and reddish-brown stained knife and tells him "I think my brother might have killed your daughter."
  The stranger's brother lived in an A-Frame house less than a mile from the crash. After that night, he remembered his brother acting
  really strange. Later he found a bloody knife in the glove compartment of his brother's car. Fred mails the knife to New Hampshire police along
  with a note explaining everything. Fred gets a confirmation letter days later confirming they've received the package. Fred never heard
  anything else about it or learned of any other lab results. He also found out that a backpack possibly belonging to Maura was found in the woods
  but didn't know anything else about it. Officials on the case have only responded, "we are aware of the backpack."
""")