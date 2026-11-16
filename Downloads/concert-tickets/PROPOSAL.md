# Project proposal

* Name: Fred Mathys Njike N.
* Project title: Concert Tickets
* Pitch (one sentence): It is a website where people can see the concerts that are coming soon and then book tickets for the one they like, without making an account.
* Target users: Students and young people who like going to concerts and who want one simple place to see what is happening and to reserve their tickets quickly.

## Pages

| URL | Content | Dynamic segment? | Rendering strategy and why |
|---|---|---|---|
| / | The home page with the list of all the concerts that are coming, each one with the artist, the city, the date and the price | No | ISR with revalidate every 60 seconds, because the list does not change every second but it should still update when someone adds a new concert, and also it is public so Google should be able to read it |
| /concerts/[id] | The page of one concert with the description, the venue, the date, the price, how many tickets are left, and the form to book tickets | Yes, [id] | Dynamic (force-dynamic), because the number of tickets left changes every time someone books, so I do not want an old number shown to the visitor |
| /concerts/new | A form to add a new concert to the website | No | Static, because it is only a form and the content never changes |
| /tickets/[id] | A confirmation page that shows the booking after someone buys a ticket, with the name, the quantity and the concert | Yes, [id] | Dynamic, because it depends on the data of one booking that was just created |
| /about | A small page that explains what the website is and how to book a ticket | No | Static, because the text never changes |

## Data

I have 2 entities and they are linked together, because one concert can have many tickets and each ticket belongs to only one concert.

* **Concert**: id, title, artist, city, venue, date, description, price, ticketsLeft
* **Ticket**: id, buyerName, email, quantity, createdAt, concertId (this one is the link to the Concert)

So the relation is one Concert to many Tickets. I will use Prisma later for this, and at the beginning I will just use a JSON file like we did in the lab.

## Write actions

Users can add a new concert with the form on /concerts/new, and they can book tickets for a concert with the form on the concert page, which creates a new Ticket and also lowers the number of tickets left. I also want to let them delete a concert, and update its information (like the price or the date) if they made a mistake, so that I have all the CRUD operations for Milestone 3. There is no login in my project, so anyone can do these actions.

## Repository

GitHub URL: https://github.com/njfred5/concert-tickets