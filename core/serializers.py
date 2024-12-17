from rest_framework import serializers
from .models import Influencer, SocialMediaAccount, Employee

class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccount
        fields = ['id', 'platform', 'username']

    def validate(self, data):
      if not data.get('platform'):
          raise serializers.ValidationError("Platform cannot be empty")
      
      if not data.get('username'):
          raise serializers.ValidationError("Username cannot be empty")
      
      return data

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'first_name', 'last_name', 'email']

    def validate_first_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("First name cannot be empty")
        
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long")
        
        return value
    
    def validate_last_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Last name cannot be empty")
        
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long")
        
        return value

class InfluencerSerializer(serializers.ModelSerializer):
    social_media_accounts = SocialMediaAccountSerializer(many=True)
    manager = EmployeeSerializer(read_only=True)
    manager_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), 
        source='manager', 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = Influencer
        fields = ['id', 'first_name', 'last_name', 'social_media_accounts', 'manager', 'manager_id']

    def validate_first_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("First name cannot be empty")
        
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters long")
        
        return value
    
    def validate_last_name(self, value):
        if not value or value.strip() == '':
            raise serializers.ValidationError("Last name cannot be empty")
        
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters long")
        
        return value

    def validate(self, data):
        if 'manager' in data:
            manager = data['manager']
            try:
                Employee.objects.get(id=manager.id)
            except Employee.DoesNotExist:
                raise serializers.ValidationError({"manager_id": "Invalid manager ID"})
        
        if 'social_media_accounts' in data:
            accounts = []
            for index, account in enumerate(data['social_media_accounts']):
                platform = account.get('platform')
                username = account.get('username')
                
                if account in accounts:
                    raise serializers.ValidationError({
                        "social_media_accounts": {f'{index}': f"Duplicate {username} in this platform"}
                    })
                accounts.append(account)
                
                if platform.lower() == 'instagram':
                    if not username.startswith('@'):
                        raise serializers.ValidationError({
                            "social_media_accounts": "Instagram username must start with @"
                        })
        
        return data

    def create(self, validated_data):
        social_accounts_data = validated_data.pop('social_media_accounts', [])
        
        manager = validated_data.pop('manager', None)
        
        influencer = Influencer.objects.create(**validated_data)
        
        if manager:
            influencer.manager = manager
            influencer.save()
        
        for account_data in social_accounts_data:
            existing_account = SocialMediaAccount.objects.filter(
                influencer=influencer,
                platform=account_data['platform'],
                username=account_data['username']
            ).exists()
            
            if not existing_account:
                SocialMediaAccount.objects.create(
                    influencer=influencer, 
                    **account_data
                )
        
        return influencer

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        
        instance.manager = validated_data.pop('manager', None)
        instance.save()
        
        social_accounts_data = validated_data.pop('social_media_accounts', [])
        if social_accounts_data:
            instance.social_media_accounts.all().delete()
            
            # Add new accounts
            for account_data in social_accounts_data:
                SocialMediaAccount.objects.create(
                    influencer=instance, 
                    **account_data
                )
        
        return instance