from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
# To avoid the name conflict of two `Note`s:
from .models import Note as NoteModel


# You have to name the class what you're going to use in
# the request, or something like that, and it will pluralize
# it, so if you want to look for "Notes" call it "Note" here
class Note(DjangoObjectType):
    class Meta:
        model = NoteModel

        # Describe the data as a node in the graph for GraphQL
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    note = graphene.Field(Note, id=graphene.String(), title=graphene.String())
    all_notes = graphene.List(Note)

    def resolve_all_notes(self, info):
        """Decide which notes to return."""

        user = info.context.user  # Use docs or debugger to find this

        if settings.DEBUG:
            return NoteModel.objects.all()
        elif user.is_anonymous:
            return NoteModel.objects.none()
        else:
            return NoteModel.objects.filter(user=user)

    def resolve_note(self, info, **kwargs):
        title = kwargs.get("title")
        id = kwargs.get('id')

        # maybe add a filter before the .get to only search the right user
        if title is not None:
            return NoteModel.objects.get(title=title)

        return None


class CreateNote(graphene.Mutation):

    class Arguments:
        # Input attributes for the mutation
        title = graphene.String()
        content = graphene.String()

    # Output fields after mutation
    ok = graphene.Boolean()
    note = graphene.Field(Note)

    def mutate(self, info, title, content):
        user = info.context.user

        if user.is_anonymous:
            is_ok = False
            return CreateNote(ok=new_ok)

        else:
            new_note = NoteModel(title=title, content=content, user=user)
            new_note.save()
            is_ok = True

            return CreateNote(note=new_note, ok=is_ok)


class Mutation(graphene.ObjectType):
    create_note = CreateNote.Field()

# Add a schema and attach the query
schema = graphene.Schema(query=Query)
