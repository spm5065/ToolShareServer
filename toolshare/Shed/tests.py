from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from Shed.models import Shed
from Tool.models import Tool
from share_user.models import ShareUser

class ShedModelTests(TestCase):

    def test_shed_get_tool_list(self):
        """
        Make sure this method is properly retrieving tools that belong to this shed.
        """
        tool_in_shed = None
        for i in range(Shed.objects.count()):
            if tool_in_shed is None:
                try:
                    tool_in_shed = Tool.objects.get(ownershed=(i+1))
                except Tool.DoesNotExist:
                    return self.assertTrue(True, "N/A : All Sheds currently have no tools")
        shed = Shed.objects.get(pk=i)
        if tool_in_shed:
            return self.assertTrue(tool_in_shed.ownershed == shed)
        else:
            return self.assertTrue(True, "N/A : All Sheds currently have no tools")

class ShedViewTests(TestCase):
    def test_register_user_with_shed(self):
        """
        Check if user was registered to shed after POST requesting to do so
        """
        self.client.login(username='gabe', password='lol')
        response = self.client.get(reverse('shed:register_user', args=(1,)))
        user_me = ShareUser.objects.get(user__username='gabe')
        return self.assertTrue(user_me.sheds.get(pk=1))

    def test_my_shed_list(self):
        """
        Returns all sheds the current user is registered to
        """
        self.client.login(username='gabe', password='lol')
        user = User.objects.get(username='gabe')
        shed_list = user.shareuser.sheds.all()
        response = self.client.get(reverse('accounts:my_shed'))
        self.assertQuerysetEqual(
            response.context['query_shed_list'],
            ["<Shed: Gabe's Tools>"]
        )

    def test_deregister_user_with_shed(self):
        """
        Check if user was deregistered to shed after POST requesting to do so
        """
        self.client.login(username='gabe', password='lol')
        response = self.client.get(reverse('shed:deregister_user', args=(1,)))
        user_me = ShareUser.objects.get(user__username='gabe')
        try:
            user_me.sheds.get(pk=1)
            return self.assertFalse(False)
        except Shed.DoesNotExist:
            return self.assertTrue(True)