# # create a group profile when a group chat is created


# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Room, GroupRoomProfile


# @receiver(post_save, sender=Room)
# def create_group(sender, instance, created, **kwargs):

#     if created and instance.group:

#         if not GroupRoomProfile.objects.filter(room=instance.id).exists():

#             GroupRoomProfile.objects.create(room=instance.id, creator=instance.members.first())

