from __future__ import unicode_literals
from itertools import chain

from django.db import migrations


def populate_permissions_lists(apps):
    permission_class = apps.get_model('auth', 'Permission')

    perm_add_account = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='account',
                                                          codename='add_account')
    perm_change_account = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='account',
                                                          codename='change_account')
    perm_view_account = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='account',
                                                          codename='view_account')

    bank_permissions = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='bank')

    perm_view_bank = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='bank',
                                                          codename='view_bank')

    card_permissions = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='card')

    perm_view_card = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='card',
                                                          codename='view_card')

    payment_permissions = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='payment method')

    perm_view_payment = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='payment',
                                                          codename='view_payment_method')

    perm_add_profile = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='profile',
                                                          codename='add_profile')

    perm_change_profile = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='profile',
                                                          codename='change_profile')

    perm_view_profile = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='profile',
                                                          codename='view_profile')

    perm_delete_profile = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='profile',
                                                          codename='delete_profile')

    perm_add_transaction = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='transaction',
                                                          codename='add_transaction')

    perm_view_transaction = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='transaction',
                                                          codename='view_transaction')

    perm_change_transaction = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='transaction',
                                                          codename='change_transaction')

    perm_delete_transaction = permission_class.objects.filter(content_type__app_label='app',
                                                          content_type__model='transaction',
                                                          codename='delete_transaction')


    normal_user_permissions = chain(perm_add_account,
                                    perm_change_account,
                                    perm_view_account,
                                    bank_permissions,
                                    card_permissions,
                                    payment_permissions,
                                    perm_add_profile,
                                    perm_change_profile,
                                    perm_view_profile,
                                    perm_add_transaction,
                                    perm_view_transaction)

    staff_permissions = chain(perm_view_account,
                              perm_view_bank,
                              perm_view_card,
                              perm_view_payment,
                              perm_view_profile,
                              perm_delete_profile,
                              perm_view_transaction,
                              perm_change_transaction,
                              perm_delete_transaction)

    my_groups_initialization_list = [
        {
            "name": "normal_user",
            "permissions_list": normal_user_permissions,
        },
        {
            "name": "staff",
            "permissions_list": staff_permissions,
        },
    ]
    return my_groups_initialization_list


def add_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    Group = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = Group.objects.get(
                name=group['name']
            )
            group_object.permissions.set(group['permissions_list'])
            group_object.save()


def remove_group_permissions_data(apps, schema_editor):
    groups_initialization_list = populate_permissions_lists(apps)

    Group = apps.get_model('auth', 'Group')
    for group in groups_initialization_list:
        if group['permissions_list'] is not None:
            group_object = Group.objects.get(
                name=group['name']
            )
            list_of_permissions = group['permissions_list']
            for permission in list_of_permissions:
                group_object.permissions.remove(permission)
                group_object.save()


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0006_update_option_names'),
    ]

    operations = [
        migrations.RunPython(
            add_group_permissions_data,
            remove_group_permissions_data
        )
    ]
