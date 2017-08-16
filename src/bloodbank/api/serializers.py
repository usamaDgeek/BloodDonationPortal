from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    EmailField,
    CharField,
)
from bloodbank.models import BloodCatalog
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

detail_url = HyperlinkedIdentityField(
        view_name="bloodcatalog-api:detail",
        lookup_field="pk",
    )


class BloodCatalogCreateUpdateSerializer(ModelSerializer):
    owner = SerializerMethodField()

    class Meta:
        model = BloodCatalog
        fields = (
            "id",
            "owner",
            "tlocation_X",
            "tlocation_Y",
        )

    def get_owner(self, obj):
        return str(obj.owner)

class BloodCatalogListSerializer(ModelSerializer):
    url = detail_url
    owner = SerializerMethodField()

    class Meta:
        model = BloodCatalog
        fields = (
            "url",
            "id",
            "owner",
            "name",
        )

    def get_owner(self, obj):
        return str(obj.owner)


class BloodCatalogDetailSerializer(ModelSerializer):
    url = detail_url
    owner = SerializerMethodField()

    class Meta:
        model = BloodCatalog
        fields = (
            "url",
            "id",
            "owner",
            "name",
            "tlocation_X",
            "tlocation_Y",
        )

    def get_owner(self, obj):
        return str(obj.owner)


class UserCreateSerializer(ModelSerializer):
    email = EmailField(label="Email Address")
    email2 = EmailField(label="Confirm Email")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "email2",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value

        if email1 != email2:
            raise ValidationError("Emails must match")

        user_qs = User.objects.filter(email=email2)

        if user_qs.exists():
            raise ValidationError("This user has already registered")

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value

        if email1 != email2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        user_obj = User(
            username=username,
            email=email,
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(allow_blank=True, required=True)
#    email = EmailField(label="Email Address", allow_blank=True, required=False)

    class Meta:
        model = User
        fields = (
            "username",
#            "email",
            "password",
            "token",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        user_obj = None
        username = data.get("username", None)
        password = data["password"]

        if not username:
            raise ValidationError("A username is required to login.")

        user = User.objects.filter(
            Q(username=username)
        )

        if user.exists():
            user_obj = user.first()
        else:
            raise ValidationError("This username is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials! Please try again.")

        data["token"] = ""
        return user_obj
