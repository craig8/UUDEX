import pytest
from sqlmodel import Session
import uudex_server.models as m
import uudex_server.repos as repo


@pytest.fixture
async def setup_data_type_and_dataset_definition(session: Session):
    data_type = m.DataTypeCreate(data_type_uuid="uuid1",
                                 data_type_name="type1",
                                 description="desc1",
                                 schema_definition="schema1",
                                 specification_reference="spec1")
    dataset_definition = m.DatasetDefinitionCreate(dataset_definition_uuid="uuid2",
                                                   dataset_definition_name="definition1",
                                                   description="desc2")
    created_data_type = await repo.DataTypeRepo.create(session, data_type)
    created_dataset_definition = await repo.DatasetDefinitionRepo.create(
        session, dataset_definition)
    return created_data_type, created_dataset_definition


@pytest.mark.asyncio
async def test_create_attached_data_type(session: Session, setup_data_type_and_dataset_definition):
    created_data_type, created_dataset_definition = setup_data_type_and_dataset_definition

    attached_data_type = m.AttachedDataTypeCreate(
        dataset_definition_id=created_dataset_definition.dataset_definition_id,
        data_type_id=created_data_type.data_type_id)
    result = await repo.AttachedDataTypeRepo.create(session, attached_data_type)
    assert result.dataset_definition_id == created_dataset_definition.dataset_definition_id
    assert result.data_type_id == created_data_type.data_type_id


@pytest.mark.asyncio
async def test_select_attached_data_type_by_ids(session: Session,
                                                setup_data_type_and_dataset_definition):
    created_data_type, created_dataset_definition = setup_data_type_and_dataset_definition

    attached_data_type = m.AttachedDataTypeCreate(
        dataset_definition_id=created_dataset_definition.dataset_definition_id,
        data_type_id=created_data_type.data_type_id)
    await repo.AttachedDataTypeRepo.create(session, attached_data_type)
    result = await repo.AttachedDataTypeRepo.select_by_ids(
        session, created_dataset_definition.dataset_definition_id, created_data_type.data_type_id)
    assert result is not None
    assert result.dataset_definition_id == created_dataset_definition.dataset_definition_id
    assert result.data_type_id == created_data_type.data_type_id


@pytest.mark.asyncio
async def test_update_attached_data_type(session: Session, setup_data_type_and_dataset_definition):
    created_data_type, created_dataset_definition = setup_data_type_and_dataset_definition

    attached_data_type = m.AttachedDataTypeCreate(
        dataset_definition_id=created_dataset_definition.dataset_definition_id,
        data_type_id=created_data_type.data_type_id)
    await repo.AttachedDataTypeRepo.create(session, attached_data_type)
    result = await repo.AttachedDataTypeRepo.select_by_ids(
        session, created_dataset_definition.dataset_definition_id, created_data_type.data_type_id)
    result.dataset_definition_id = created_dataset_definition.dataset_definition_id
    updated_result = await repo.AttachedDataTypeRepo.update(session, result)
    assert updated_result.dataset_definition_id == created_dataset_definition.dataset_definition_id


@pytest.mark.asyncio
async def test_delete_attached_data_type(session: Session, setup_data_type_and_dataset_definition):
    created_data_type, created_dataset_definition = setup_data_type_and_dataset_definition

    attached_data_type = m.AttachedDataTypeCreate(
        dataset_definition_id=created_dataset_definition.dataset_definition_id,
        data_type_id=created_data_type.data_type_id)
    await repo.AttachedDataTypeRepo.create(session, attached_data_type)
    attached_data_type_remove = m.AttachedDataTypeRemove(
        dataset_definition_id=created_dataset_definition.dataset_definition_id,
        data_type_id=created_data_type.data_type_id)
    await repo.AttachedDataTypeRepo.delete(session, attached_data_type_remove)
    result = await repo.AttachedDataTypeRepo.select_by_ids(
        session, created_dataset_definition.dataset_definition_id, created_data_type.data_type_id)
    assert result is None
