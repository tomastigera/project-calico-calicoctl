from test_base import TestBase
from docker_host import DockerHost


class TestProfileCommands(TestBase):
    def test_profile_commands(self):
        """
        Test that the profile rule update command successfully updates.
        """
        host = DockerHost('host')

        calicoctl = "/code/dist/calicoctl %s"
        host.execute(calicoctl % "profile add TEST_PROFILE")

        json = ('{ "id": "TEST_PROFILE", '
                  '"inbound_rules": [ { "action": "allow", "src_tag": "TEST_PROFILE" }, '
                                     '{ "action": "deny" } ], '
                  '"outbound_rules": [ { "action": "deny" } ] }')
        host.execute("echo '%s' | " % json + calicoctl % "profile TEST_PROFILE rule update")

        self.assertIn('1 deny', host.execute(calicoctl % "profile TEST_PROFILE rule show").stdout.rstrip())
        json_piece = '"outbound_rules": [\n    {\n      "action": "deny"'
        self.assertIn(json_piece, host.execute(calicoctl % "profile TEST_PROFILE rule json").stdout.rstrip())

        # Test that adding and removing a tag works.
        self.assertNotIn("TEST_TAG", self.show_tag(host))
        host.execute(calicoctl % "profile TEST_PROFILE tag add TEST_TAG")
        self.assertIn("TEST_TAG", self.show_tag(host))
        host.execute(calicoctl % "profile TEST_PROFILE tag remove TEST_TAG")
        self.assertNotIn("TEST_TAG", self.show_tag(host))

    def show_tag(self, host):
        calicoctl = "/code/dist/calicoctl %s"
        return host.execute(calicoctl % "profile TEST_PROFILE tag show").stdout.rstrip()