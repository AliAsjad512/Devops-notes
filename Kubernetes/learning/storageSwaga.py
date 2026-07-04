💾 The Storage Saga
Core Concepts - Episode 8 of 15
Tuesday afternoon. Agastya proudly deployed a MySQL database in Kubernetes. The pod was running perfectly. He inserted some test data - user records, product information, orders. Everything worked beautifully.

Then disaster struck. The pod crashed due to an out-of-memory error. Kubernetes auto-healed it by creating a new pod. Agastya checked the database and...

ALL DATA WAS GONE! Every table was empty. The new pod started with a fresh, empty database.

He rushed to Vashisht in panic: "Sir, I thought Kubernetes was production-ready! How can all our data disappear when a pod restarts? This is a disaster!"

👨‍💻 Agastya
Crisis Mode: Lost all database data on pod restart!
Confusion: "Why doesn't Kubernetes save my data?"
🎓 Vashisht
Teaching Today: Persistent storage fundamentals
Mission: Understanding stateful workloads
👨‍🏫 Nandan
Role: Storage architecture deep-dive
Focus: PV, PVC, StorageClass