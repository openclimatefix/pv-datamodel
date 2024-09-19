from pvsite_datamodel import UserSQL, SiteGroupSQL
from pvsite_datamodel.read import get_user_by_email
from pvsite_datamodel.write.user_and_site import create_site_group, create_user


class TestGetUserByEmail:
    """Test for get_user_by_email function"""
    def test_get_user_by_email_no_users_site_group_exists(self,db_session):
        site_group = create_site_group(db_session=db_session,site_group_name="site_group_for_test@test.com")
        user = get_user_by_email(session=db_session, email="test@test.com")
        assert len(db_session.query(UserSQL).all()) == 1
        assert len(db_session.query(SiteGroupSQL).all()) == 1
    def test_get_user_by_email_no_users(self, db_session):
        user = get_user_by_email(session=db_session, email="test@test.com")
        assert user.email == "test@test.com"
        assert len(db_session.query(UserSQL).all()) == 1

    def test_get_user_by_email_with_users(self, db_session):
        site_group = create_site_group(db_session=db_session)
        user = create_user(
            session=db_session, site_group_name=site_group.site_group_name, email="test_1@test.com"
        )
        user = create_user(
            session=db_session, site_group_name=site_group.site_group_name, email="test_2@test.com"
        )

        user = get_user_by_email(session=db_session, email="test_1@test.com")
        assert user.email == "test_1@test.com"
        assert len(db_session.query(UserSQL).all()) == 2

    def test_get_user_by_email_no_user_maker_user_false(self, db_session):
        user = get_user_by_email(
            session=db_session, email="test@test.com", make_new_user_if_none=False
        )
        assert user is None
        assert len(db_session.query(UserSQL).all()) == 0
