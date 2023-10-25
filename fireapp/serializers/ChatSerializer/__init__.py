from rest_framework import serializers
from fireapp.models import ChatModel


class ChatSerializer(serializers.ModelSerializer):
    receiver_id = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'text', 'placeholder': 'User ID'}
    )

    message = serializers.CharField(
        write_only=True,
        required=True,
        help_text="""<h4>Sign in using custom tokens on clients</h4><p>The client app authenticates with the custom 
        token by calling <code translate="no" dir="ltr">signInWithCustomToken()</code>: <a 
        href="https://firebase.google.com/docs/auth/admin/create-custom-tokens#sign_in_using_custom_tokens_on_clients 
        " target="_blank">Learn more</a>, see the <a 
        href="https://codesandbox.io/s/signinwithcustomtoken-zk54c3?file=/src/index.js" 
        target="_blank">Example</a></p>""",
        style={'input_type': 'text', 'placeholder': 'Message', }
    )

    class Meta:
        model = ChatModel
        fields = ('receiver_id', 'message')
