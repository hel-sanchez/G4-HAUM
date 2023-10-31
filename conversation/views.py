from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from conversation.forms import ConversationMessageForm
from conversation.models import Conversation
from item.models import Item


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if item.created_by == request.user:
        return redirect('conversation:detail_conversation', pk=item_pk)

    # Check if there is an existing conversation or create a new one
    conversation = Conversation.objects.filter(item=item, members=request.user).first()

    if conversation is None:
        conversation = Conversation.objects.create(item=item)
        conversation.members.add(request.user)
        conversation.members.add(item.created_by)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.sender = request.user
            conversation_message.save()

            # Unmark the conversation as deleted (if it was deleted previously)
            conversation.deleted_by.remove(request.user)
            return redirect('conversation:detail_conversation', pk=conversation.pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/new_conversation.html', {
        'form': form,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members=request.user).exclude(deleted_by=request.user)

    return render(request, 'conversation/inbox.html', {
        'conversations': conversations,
    })


@login_required
def detail_conversation(request, pk):
    conversation = Conversation.objects.filter(members=request.user).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.sender = request.user
            conversation_message.save()

            # Do not mark the conversation as deleted for the current user
            # This way, the conversation will remain visible to the user who replied
            # and it won't disappear
            # conversation.deleted_by.add(request.user)  # Comment out this line

            # Ensure that the conversation is not deleted for other members
            other_members = conversation.members.exclude(pk=request.user.pk)
            conversation.deleted_by.remove(*other_members)

            return redirect('conversation:detail_conversation', pk=conversation.pk)

    else:
        form = ConversationMessageForm()

    return render(request, 'conversation/detail_conversation.html', {
        'conversation': conversation,
        'form': form,
    })


@login_required
def delete_conversation(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)

    # Check if the logged-in user is a member of the conversation
    if request.user in conversation.members.all():
        # Mark the conversation as deleted only for the current user
        conversation.deleted_by.add(request.user)
        messages.success(request, "Conversation removed from inbox.")
    else:
        messages.error(request, "You do not have permission to delete this conversation.")

    return redirect('conversation:inbox')