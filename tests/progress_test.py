import pytest
from bdd.progress import find_prev_and_next, summarize_course_progress

mockProgressReal = {
    "CourseUUID": "3b39d0f6-f944-4f1b-832d-a1daba32eda4",
    "Chapters": [
        {
            "UUID": "9e6acea2-8081-404d-9c34-3b5f677fa580",
            "Title": "Variables",
            "Lessons": [
                {
                    "UUID": "224252be-adc9-452f-8ed0-0b305b25d0cb",
                    "Title": "Learn Go (for Developers)",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "a1eae01c-0a40-47d5-9b98-94fe48199073",
                    "Title": "Basic Variables",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "62881ae0-89f4-44e6-b69e-50a7652a7da3",
                    "Title": "Short Variable Declaration",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "73145333-7245-4643-ae6b-e65a5f719906",
                    "Title": "Why Go?",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "a581676a-054c-4c8f-a95d-396d626b0803",
                    "Title": "Comments",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "ecc34f1e-1b3c-41af-85bb-aee7ddb4006b",
                    "Title": "The Compilation Process",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "9180f35f-79cb-4df8-b561-c370b15dba95",
                    "Title": "Fast and compiled",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "01660f75-10e9-4410-abf5-f2f33f4f6e2a",
                    "Title": "Type Sizes",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "98e60d90-0111-4626-a690-70124be1e0ba",
                    "Title": "Which Type Should I Use?",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "fc3fe54e-6106-44a6-abe0-7cf2961c240c",
                    "Title": "Which Type Should I Use?",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b0807eaa-38e5-4d3f-8359-ffe5e1c9ae7e",
                    "Title": "Go is Statically Typed",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "723bcd30-be47-4663-85b6-eb348abcf53f",
                    "Title": "Compiled vs Interpreted",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "4c0f0f05-38dc-45c3-af26-802434325407",
                    "Title": "Compiled vs Interpreted",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "6725ea2b-ce54-443f-a304-5ae8138b31eb",
                    "Title": "Same Line Declarations",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "a011d7b7-209e-43ff-8d6a-aefa26e9772f",
                    "Title": "Small memory footprint",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "342ad08b-b3a0-41c6-8803-f5c86e23382d",
                    "Title": "Small memory footprint",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "30beb009-2e1c-4cae-98b2-e9738101cd56",
                    "Title": "Constants",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "8abcb4c0-c9c3-42dd-8a5b-61a7900032d2",
                    "Title": "Computed Constants",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "162d016b-c9b3-4a14-9be2-fd22c74c5710",
                    "Title": "Comparing Go's Speed",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f9aceb0e-b830-480a-bd99-145c1485524c",
                    "Title": "Formatting Strings in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "4ae3622b-70b8-45f9-84ee-9822e44c0fbc",
                    "Title": "Runes and String Encoding",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b72beb2f-138b-4806-8aea-52609bb35b74",
                    "Title": "Fix more bugs",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "22b72d79-74ef-46c1-88f4-e0440df0d48e",
                    "Title": "Fix types",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "1d7863f1-0a93-423e-9047-8448af33cda8",
                    "Title": "Type Inference",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "fb9983c3-11c0-4ba3-993f-0df0629c2643",
                    "Title": "Format practice",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "e784c584-f6a7-4c21-bcef-a6c800aa4491",
            "Title": "Conditionals",
            "Lessons": [
                {
                    "UUID": "e210dea3-0c70-41c1-871b-4aa5b3658917",
                    "Title": "Conditionals",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "84e5481a-ca9c-40a3-ad0f-64d275226859",
                    "Title": "The initial statement of an if block",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "40827535-320e-463b-850a-bb6ffe8082e8",
                    "Title": "The initial statement of an if block",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f8b2fcea-078b-41be-b59b-8bece5ae923b",
                    "Title": "Switch",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f6c53b4a-3bfe-49ca-8733-aa15c19fe7b1",
                    "Title": "Calculate Balance",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "10b92b5a-6687-474e-9df0-e215b7d0a46d",
            "Title": "Functions",
            "Lessons": [
                {
                    "UUID": "9aedf839-7d94-43f7-82d0-1d27e5d0b79c",
                    "Title": "Functions",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7f503d3f-7425-496a-b50a-70815384a00c",
                    "Title": "Multiple Parameters",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "a729ff01-7620-45a6-b330-7efb72bda67b",
                    "Title": "Unit Test Lessons",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "afb405db-9785-4444-94f5-e76866b5b6b7",
                    "Title": "Declaration Syntax",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "34172c62-9ae4-46ec-88d8-d8bdeab39eb4",
                    "Title": "Declaration Syntax",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "221e3837-4eba-4171-a3fc-b32a1b3cd423",
                    "Title": "Declaration Syntax",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "351c4674-1c31-4148-b98f-1179dbcaac81",
                    "Title": "Passing Variables by Value",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "185e65bf-8d3a-4419-abd0-258a457f0b88",
                    "Title": "Ignoring Return Values",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "bfd3eabd-58f5-4fe1-b59d-876b83bf52e8",
                    "Title": "Named Return Values",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "27adecfc-463c-464f-9dc0-d8a4fa588c93",
                    "Title": "The Benefits of Named Returns",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "917d5454-6e71-4e27-a872-d5f6562181ce",
                    "Title": "The Benefits of Named Returns",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "067df3cb-a240-4f10-8159-b04a737e5002",
                    "Title": "Explicit Returns",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b91b68e4-3cad-4185-bc82-f1db1a2cea0e",
                    "Title": "Early Returns",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "498e1d59-9dff-4da6-8848-755aff061d37",
                    "Title": "Early Returns",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "3c0f1141-9d3e-4acd-bfe8-1ebf1b44121e",
                    "Title": "Functions as values",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b79955b7-eccf-4816-8490-1dd700f13c8e",
                    "Title": "Anonymous Functions",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "8ea7016d-a2fd-4900-b10d-178d6e8b2ecb",
                    "Title": "Defer",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "43edcbd3-d84b-432e-898c-62b1463aca34",
                    "Title": "Block Scope",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "a800cb84-5d09-4635-941a-93a0c90f9f06",
                    "Title": "Billing System",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "09628165-d910-4344-b2bf-c9145d6e6317",
                    "Title": "Processing Orders",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "f2c926e4-4e10-40d3-bffb-11683a8c3c1f",
                    "Title": "Closures",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "59d90390-f479-4472-bb16-9af599285229",
            "Title": "Structs",
            "Lessons": [
                {
                    "UUID": "81362a78-09b3-459e-bd16-c0312d3ef2d2",
                    "Title": "Structs in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "525b8c5b-ab89-4588-8117-f91e81b778bc",
                    "Title": "Nested structs in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7256e43f-aea0-47bb-9671-9c55ebca7095",
                    "Title": "Anonymous Structs in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "164543d4-09d7-4aec-92b3-4a695dad988d",
                    "Title": "Anonymous Structs in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "e30f8be3-30e4-4528-ab93-54461538314e",
                    "Title": "Embedded Structs",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "57ab6160-2769-4e7a-859c-6c4222768fdd",
                    "Title": "Struct methods in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "84de8a08-1f02-47fd-b0a9-cab314162722",
                    "Title": "Memory Layout",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ed8c47e7-7d04-4e2c-89ed-9cf9ea23f3d5",
                    "Title": "Empty Struct",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "582eaa7b-229f-4bac-884c-ff2d4089c1f5",
                    "Title": "Empty Struct",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "cdc70166-9a08-4536-a7f3-b497ea23a056",
                    "Title": "Update users",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "bdaf1d5b-5471-49ed-8a73-30a09b9140ef",
                    "Title": "Send Message",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "7faa7ccf-4fc0-406d-90b7-dac16e72f6c3",
            "Title": "Interfaces",
            "Lessons": [
                {
                    "UUID": "efcafed8-c0ba-4efb-a6e2-88db3c8a0733",
                    "Title": "Interfaces in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "8c123c3a-46d5-46d3-a4c4-d1e2555af05b",
                    "Title": "Interface Implementation",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "bba3754d-08a0-460c-9a3a-e7d0e304e290",
                    "Title": "Interfaces are implemented implicitly",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "428cab40-448d-4467-9c53-ab880301e34b",
                    "Title": "Interfaces are implemented implicitly",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "97fb43cb-9f0e-43a2-9510-7d620352cd79",
                    "Title": "Interfaces Quiz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "29421b9a-eab6-4051-8ff7-c84592107b1a",
                    "Title": "Interfaces Quiz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "59b4509c-0cb1-487f-8b3f-68357629e60e",
                    "Title": "Multiple Interfaces",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "57e27288-cfeb-412f-9c75-18748ca11c69",
                    "Title": "Name Your Interface Arguments",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "2a389003-c96c-4b48-9cb3-d25f45e51c22",
                    "Title": "Name Your Interface Arguments",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7804ef9a-1a03-42a0-94d1-42ca09b89e43",
                    "Title": "Type assertions in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "c144048b-e074-4573-b6dd-c90ad9ca8b76",
                    "Title": "Type Switches",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "d4e52816-6e2e-475b-a9a0-6c350096b6f3",
                    "Title": "Clean Interfaces",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "93a21c7a-9d6e-4794-a4b9-c6010627ee43",
                    "Title": "Clean Interfaces",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "83f82b16-9d9b-48fa-8033-1d04e367f439",
                    "Title": "Clean Interfaces",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "5498d6da-38ea-4993-bc88-cc5f07eff909",
                    "Title": "Clean Interfaces",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "4988b18c-4da4-4f55-84fb-25096dcc66c2",
                    "Title": "Message Formatter",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "7af7c74b-99bb-4420-9fa4-275fb8ec7a5a",
                    "Title": "Process Notifications",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "238a836c-56a2-4e0d-8e32-fd796a145272",
            "Title": "Errors",
            "Lessons": [
                {
                    "UUID": "1aac4f6b-8416-4a67-a1f7-fb46bcb11565",
                    "Title": "The Error Interface",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ca45d3a1-74f7-49e9-92ba-0e0b66c032fa",
                    "Title": "Formatting strings review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "9593d446-087e-438d-8c7e-caa8b4a8ab4d",
                    "Title": "The Error Interface",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "6bd24309-d380-4f0e-afd1-c4d7915c3281",
                    "Title": "Errors Quiz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "5c815f18-1f21-4dea-83d7-636956abe992",
                    "Title": "Errors Quiz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "8a7cb390-19f1-4ddb-8758-292d7577e69e",
                    "Title": "The Errors Package",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "97d11d81-67a5-4b03-b2ed-65096c508b11",
                    "Title": "Panic",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "c6c9a896-4816-48f2-ae5c-16b3a117cd7f",
                    "Title": "Panic",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "1b5764f3-da60-4d1f-b917-8dc0cb12a49a",
                    "Title": "User Input",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "eeb7c86b-9544-4ce9-81d4-6d4de1414a4f",
            "Title": "Loops",
            "Lessons": [
                {
                    "UUID": "d8b6aaab-5a7c-4fb9-b8d8-82297029057a",
                    "Title": "Loops in Go",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "815d29fd-b5dc-488a-a40f-2e3a6da6eb3b",
                    "Title": "Omitting conditions from a for loop in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "98deff0a-61b4-4292-8e7a-c32554186e15",
                    "Title": "There is no while loop in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "3ddbb7dc-5669-4e14-aa81-6bec8e23ea32",
                    "Title": "Fizzbuzz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "5b5123f4-8632-4e91-9045-a7e604aba7d2",
                    "Title": "Continue & Break",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "e89a0db3-f9b5-4d17-bc68-28878f65e25f",
                    "Title": "Packet Size",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "9646a1d9-c092-49a6-98b5-794836615adb",
            "Title": "Slices",
            "Lessons": [
                {
                    "UUID": "e7ce17e4-44cd-4363-adc5-8342a8026c6e",
                    "Title": "Arrays in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "23315526-143d-4f0b-ac58-dd8a13f7cd8d",
                    "Title": "Slices in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "c5c00980-4e73-422b-9df6-a51814102a79",
                    "Title": "Slices Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "2eccae0b-0b07-4ea3-a42e-fc054566cda1",
                    "Title": "Slices Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "61959988-ef90-488e-b0aa-a03a2d283106",
                    "Title": "Slices Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "1d593952-7c0c-460b-a0d6-c41a39cbd08a",
                    "Title": "Make",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "cd6d1334-af5f-498b-b33d-47d170950208",
                    "Title": "Len and Cap Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ade1fd9c-25e8-412a-a539-e2cc2261275e",
                    "Title": "Len and Cap Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "db7e02a7-07f9-4789-a89b-528194207f59",
                    "Title": "Len and Cap Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "21f7d253-a275-49ea-a0b7-82c94afc70a6",
                    "Title": "Variadic",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "6b3853e2-5ee7-4322-bb77-a74d4375acb7",
                    "Title": "Append",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ce8736ca-c203-4cb5-ace0-1c5294f98941",
                    "Title": "Slice of slices",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f100f470-4a34-4c10-8035-551e1a8e1834",
                    "Title": "Tricky Slices",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "d65a40d0-8609-4113-affe-66c348892310",
                    "Title": "Tricky Slices",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "1e527685-da40-4525-932d-56e21e775fd4",
                    "Title": "Tricky Slices",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "bab7a065-eb05-4e63-b923-7812810be1ec",
                    "Title": "Range",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b9a645af-def3-4f69-92f1-4460413819f8",
                    "Title": "Message Filter",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "0e0b2f2c-141d-4de8-a1e0-1fbac7f5d60f",
                    "Title": "Password Strength",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "129d9a6f-1b4b-4fbd-92c9-6bb70850e29d",
                    "Title": "Mailio",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "4d3133bd-19da-4430-bbfd-acbc1f5924ec",
                    "Title": "Print Reports",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "14d7511c-6487-4861-8be7-c490ba7c7f8a",
                    "Title": "Message tagger",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "00e74458-f6e2-4f14-bc04-5ad5112551d6",
                    "Title": "Currying",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "d08e4dde-e310-4626-ae44-5c414c5b7043",
            "Title": "Maps",
            "Lessons": [
                {
                    "UUID": "5adaa6ce-c4f1-4f84-b88b-5b19542fc3ad",
                    "Title": "Maps",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "2b0807c2-7b0a-4b3e-a16d-26266dcbc460",
                    "Title": "Mutations",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "96440168-ea36-469d-b617-bc3823a77f88",
                    "Title": "Key Types",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "94309851-18a5-433e-91db-788597fda6c1",
                    "Title": "Key Types",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7ef74256-b1aa-4f4f-b0d4-0c6148d455e2",
                    "Title": "Count Instances",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "40742340-b796-46e6-a893-c3d27c86c15d",
                    "Title": "Effective Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "bcaf1729-025b-4315-a4e4-523501abae4f",
                    "Title": "Effective Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7f86be5b-ca9f-47fa-98e3-a2507749ac6f",
                    "Title": "Effective Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "2003e4c6-5f00-4b10-8ef4-597234b2762f",
                    "Title": "Effective Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "67c33818-a380-4d58-90bd-1d1804c88388",
                    "Title": "Nested",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "148a3df0-1788-41a1-9bd0-2fe758ff4ab5",
                    "Title": "Distinct Words",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "bf917002-a5c9-4de8-89ef-b70edf84f4ff",
                    "Title": "Suggested Friends",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "9183a6da-85b2-4d36-8764-af663567ebf1",
                    "Title": "Log and Delete",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "cf9303e7-45a2-4ecb-8b89-847832112f79",
            "Title": "Pointers",
            "Lessons": [
                {
                    "UUID": "7598b82d-2f83-4413-8508-a7295df86273",
                    "Title": "Introduction to Pointers",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "fa33b62c-acc3-4d4f-ab34-0d18c90fef3b",
                    "Title": "References",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "9be9e83f-46e2-444a-97a3-e9431aac938c",
                    "Title": "Pass by Reference",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b6b2daa2-c718-4dbd-937c-a50a0fa95ee7",
                    "Title": "Pointers Quiz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f44a7a7e-54a1-4274-80d1-ea36ff3b3df2",
                    "Title": "Pointers Quiz",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "88624902-f053-41da-b04a-6563d3599323",
                    "Title": "Nil Pointers",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ffe41611-1057-4ff6-8f1b-859267db5a60",
                    "Title": "Pointer Receivers",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b57c7224-fcdd-4dbc-8a2e-9b3ae1a36108",
                    "Title": "Pointer Receiver Code",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "6c3db4b9-3058-4b2f-8f32-19bd66a7356e",
                    "Title": "Pointer Performance",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "53a8b432-2bfa-4a59-9890-fe00c9580500",
                    "Title": "Pointer Performance",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "d18a3517-189b-4b04-87a2-5c3cdadaddda",
                    "Title": "Update Balance",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "5366184e-931d-4e30-80b4-f0ccde502d79",
            "Title": "Packages and Modules",
            "Lessons": [
                {
                    "UUID": "19ee5098-d35e-47ab-ad9f-cda126ff54f0",
                    "Title": "Packages",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "58dfc9ca-4403-4f58-8c34-1ce98f66ba76",
                    "Title": "Package Naming",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "35cde4a3-07d6-4f5a-98be-27677add6039",
                    "Title": "Package Naming",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "148c8301-4cda-46fc-9a4f-6613c647939c",
                    "Title": "Install",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "372137f0-b770-4e83-a965-c6205a3ccf19",
                    "Title": "Modules",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ed9a0943-6ade-4fc2-9e60-ce712bee85c3",
                    "Title": "Modules",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b7a128bb-f552-435f-b10b-16a865f7a399",
                    "Title": "Modules",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "a902f23d-df4e-4bc7-ade5-ee5372ea21ed",
                    "Title": "Setting up your machine",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7dc6a0c9-d3d8-4536-8e88-ca88fee35049",
                    "Title": "First Local Program",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "52dda666-1573-49c3-a1b2-cb54bbf892e9",
                    "Title": "Go Run",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "54c794e4-55d8-4c43-8d95-b22a3ebdca2f",
                    "Title": "Go Build",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "576b7605-b5d7-42aa-92a9-7c8e63929a09",
                    "Title": "Go Install",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "2c32a5fc-6827-48f9-a033-392881ff3ca5",
                    "Title": "Custom Package",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "5e5236b3-9ce4-45de-8759-ac3afabf0cbb",
                    "Title": "Custom Package Continued",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "9c49ad86-aee5-4f56-8df2-59ae5cdb194d",
                    "Title": "Remote Packages",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "665767ab-dab2-48e5-88b7-1534d24553f8",
                    "Title": "Clean Packages",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "6dfe4969-745b-4a62-a23c-b255afacf760",
                    "Title": "Clean Packages",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f7bff17d-0974-4580-9c5b-b0080144970b",
                    "Title": "Clean Packages",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "ba188ac9-c0f7-477f-bad1-4a11e4f9086e",
            "Title": "Channels",
            "Lessons": [
                {
                    "UUID": "ae21fb67-6443-4b43-b569-14b452872311",
                    "Title": "Concurrency",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "04984711-09c4-4020-ac36-6d4214012d34",
                    "Title": "Channels",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "9c6f7fc9-8e7a-4857-8b10-70f130410700",
                    "Title": "Channels",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "d2a10614-3142-4d3e-906e-5a817aa920b3",
                    "Title": "Buffered Channels",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "bb1f32af-1ca2-4d6e-9bb1-226d9bb12321",
                    "Title": "Closing channels in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "31423b30-637e-480f-b2af-4e7acf3080a2",
                    "Title": "Range",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "7bcb6f15-3886-4e81-b00f-26fa907d449a",
                    "Title": "Select",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "25200976-df67-4186-9333-2996d26f25a0",
                    "Title": "Select Default Case",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "1f2da05c-9dda-4759-a237-74fab3dac89a",
                    "Title": "Channels Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "f21222a0-6a5d-4a87-bdd4-a6b317c4359d",
                    "Title": "Channels Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "275ca1c0-2219-46e7-b530-a773268de5c8",
                    "Title": "Ping Pong",
                    "IsRequired": False,
                    "IsComplete": False,
                },
                {
                    "UUID": "632572a1-847b-4691-a1d0-75ff832ab5fd",
                    "Title": "Process Messages",
                    "IsRequired": False,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "33367e35-0269-48e0-aa81-c0371524ad8c",
            "Title": "Mutexes",
            "Lessons": [
                {
                    "UUID": "720b45b3-4d5f-421c-afd7-30718166fbd4",
                    "Title": "Mutexes in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "86bdf4e1-66bc-46c7-8858-daaddb701c72",
                    "Title": "Why is it called a 'mutex'?",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "58d7347d-07c7-4752-b9b2-49ae8688c79a",
                    "Title": "Mutex Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "b13a7ce3-1bf8-4d44-b0aa-00425bc01c87",
                    "Title": "Mutex Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "c9085b04-22e5-446c-8811-5b15fb343be0",
                    "Title": "RW Mutex",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "ea7f0727-d6e2-4756-9401-5dc069292e07",
                    "Title": "Read/Write Mutex Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "893492fb-225c-45aa-9b01-d40718dfdcc8",
                    "Title": "Read/Write Mutex Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "1ec58cee-e8a0-43d2-95a2-ed709041b7e6",
                    "Title": "Read/Write Mutex Review",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "ba8aefe0-ccb8-4de7-94c1-79c8110c712e",
            "Title": "Generics",
            "Lessons": [
                {
                    "UUID": "c8999752-768a-401b-b881-602929927699",
                    "Title": "Generics in Go",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "0623b02c-537e-4696-8ec2-c60246496262",
                    "Title": "Why Generics?",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "3c78cfd6-34dc-44d9-b48d-047ca7760e66",
                    "Title": "Why Generics?",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "af6e1109-5a2b-442d-82f9-115ef8157650",
                    "Title": "Why Generics?",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "371d69ad-367e-4b7a-bd2d-a7f06a4ff0bd",
                    "Title": "Constraints",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "e69f360e-5d95-41db-96d7-a60f2d821a15",
                    "Title": "Interface type lists",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "4a9635d1-9bd9-40b4-81b7-d3662aa3889c",
                    "Title": "Parametric Constraints",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "eff5e0e9-7efa-4d36-b822-9fe636ef1066",
                    "Title": "Naming Generic Types",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "8c934735-383b-4174-af23-b782d10e5913",
            "Title": "Enums",
            "Lessons": [
                {
                    "UUID": "43b502da-2aca-4f94-8a8d-f3da2f04cec6",
                    "Title": "Lack of Enums",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "a5a082e3-5be5-4fc1-9245-7495f61baad6",
                    "Title": "Type Aliases",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "be38a2c4-3c53-42d8-8c5d-19f3824af25d",
                    "Title": "Type Aliases",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "87341ea8-9826-455c-97c2-eab4e8522ed7",
                    "Title": "Iota",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "8d144adc-73ab-4d8a-b66f-51d7c2ad378d",
            "Title": "Quiz",
            "Lessons": [
                {
                    "UUID": "318982b0-dca9-4381-96d4-96488ec8f23d",
                    "Title": "Go Proverbs",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "5d630eec-faeb-4e9b-8adb-99d8e855c913",
                    "Title": "Go Proverbs",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "6b4412b9-42e9-4b75-b02a-563950971722",
                    "Title": "Go Proverbs",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "03aa8e60-709b-46f4-9e72-49fcdb4feccb",
                    "Title": "Go Proverbs",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
    ],
}


def test_summarize_progress():
    get_progress = lambda: mockProgressReal
    uuid = "98e60d90-0111-4626-a690-70124be1e0ba"

    actual = summarize_course_progress(uuid, get_progress)
    assert len(actual) == 16
    assert actual[0][0] == "Variables"
    assert actual[0][1]  # is active
    assert actual[0][2].n_required == 21
    assert actual[0][2].n_required_complete == 8
    assert actual[0][2].n_optional_complete == 0
    assert actual[0][2].n_total == 25
    assert len(actual[0][3]) == 25
    first_lesson_in_active = actual[0][3][0]
    assert not first_lesson_in_active[0]
    assert first_lesson_in_active[1] == "Learn Go (for Developers)"
    assert first_lesson_in_active[2]
    assert first_lesson_in_active[3]

    assert not actual[1][1]  # is not active


mockProgressSimplified = {
    "CourseUUID": "course-uuid",
    "Chapters": [
        {
            "UUID": "c1",
            "Title": "c1",
            "Lessons": [
                {
                    "UUID": "l1",
                    "Title": "l1",
                    "IsRequired": True,
                    "IsComplete": True,
                },
                {
                    "UUID": "l2",
                    "Title": "l2",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
        {
            "UUID": "c2",
            "Title": "c2",
            "Lessons": [
                {
                    "UUID": "l3",
                    "Title": "l3",
                    "IsRequired": True,
                    "IsComplete": False,
                },
                {
                    "UUID": "l4",
                    "Title": "l4",
                    "IsRequired": True,
                    "IsComplete": False,
                },
            ],
        },
    ],
}


@pytest.mark.parametrize(
    "lesson_uuid, expected",
    [
        ("l1", (None, "l2")),
        ("l2", ("l1", "l3")),
        ("l3", ("l2", "l4")),
        ("l4", ("l3", None)),
    ],
)
def test_find_prev_and_next(lesson_uuid, expected):
    actual = find_prev_and_next(lesson_uuid, mockProgressSimplified)
    assert actual == expected
